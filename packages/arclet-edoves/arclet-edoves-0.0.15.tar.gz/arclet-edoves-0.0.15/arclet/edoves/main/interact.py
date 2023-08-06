from inspect import isclass
from typing import Dict, Type, Union, TypeVar, Optional, TypedDict, List, Callable, Coroutine
from .component import Component, MetadataComponent
from .behavior import BaseBehavior
from .utilles import IOStatus

TC = TypeVar("TC", bound=Component)


class Relationship(TypedDict):
    parents: Dict[str, "InteractiveObject"]
    children: Dict[str, "InteractiveObject"]


class InteractiveMeta(type):
    __check_tags__ = []

    def __instancecheck__(self, instance):
        if super(InteractiveMeta, self).__instancecheck__(instance):
            if self.__check_tags__:
                tag = self.__check_tags__.pop(0)
                if not instance.compare(*tag):
                    return False
            return True


class InteractiveObject(metaclass=InteractiveMeta):
    prefab_behavior: Type[BaseBehavior] = BaseBehavior
    prefab_metadata: Type[MetadataComponent] = MetadataComponent
    _components: Dict[str, Component]
    metadata: prefab_metadata
    behavior: prefab_behavior
    relation: Relationship

    __slots__ = "metadata", "behavior", "_components", "relation"

    __ignore__ = ["_components", "relation"]

    def __new__(cls, *args, **kwargs):
        __anno = {}
        for a in [m.__annotations__ for m in cls.__mro__[-2::-1]]:
            __anno.update(a)
        for __k in cls.__slots__:
            if __k in cls.__ignore__:
                continue
            if not issubclass(__anno[__k], Component):
                raise ValueError
        return super().__new__(cls)

    def __init__(
            self,
            metadata: Optional[Union[prefab_metadata, Type[prefab_metadata]]] = None,
            behavior: Optional[Union[prefab_behavior, Type[prefab_behavior]]] = None
    ):
        self._components = {}
        self.relation = {"parents": {}, "children": {}}
        self.metadata = (
            metadata(self) if isclass(metadata) else metadata
        ) if metadata else self.prefab_metadata(self)
        self.metadata.state = IOStatus.ACTIVATE_WAIT
        self.behavior = (
            behavior(self) if isclass(behavior) else behavior
        ) if behavior else self.prefab_behavior(self)

    def compare(self, *tag: str):
        """对比输入的tag是否存在于该IO的tags中"""
        return set(self.metadata.tags).issuperset(tag)

    def add_tags(self, *tag: str):
        """为该IO添加tag"""
        self.metadata.add_tags(tag)

    def remove_tags(self, *tag: str):
        """移除该IO的tag"""
        self.metadata.remove_tags(tag)

    def set_prime_tag(self, tag: str):
        """设置首要tag"""
        if self.compare(tag):
            index = self.metadata.tags.index(tag)
            self.metadata.tags[0], self.metadata.tags[index] = self.metadata.tags[index], self.metadata.tags[0]
        else:
            self.metadata.tags.append(tag)
            self.metadata.tags[0], self.metadata.tags[-1] = self.metadata.tags[-1], self.metadata.tags[0]

    @property
    def prime_tag(self):
        if self.metadata.tags:
            return self.metadata.tags[0]

    @property
    def parents(self):
        return self.relation['parents']

    @property
    def children(self):
        return self.relation['children']

    def filter_parents(self, *tag):
        """根据tag来对该IO的父级IO过滤"""
        return list(filter(lambda x: x.compare(*tag), self.parents.values()))

    def filter_children(self, *tag):
        """根据tag来对该IO的子级IO过滤"""
        return list(filter(lambda x: x.compare(*tag), self.children.values()))

    def set_parent(self, parent: "InteractiveObject"):
        parent.relation['children'].setdefault(self.metadata.identifier, self)
        self.relation['parents'].setdefault(parent.metadata.identifier, parent)

    def set_child(self, child: "InteractiveObject"):
        child.relation['parents'].setdefault(self.metadata.identifier, self)
        self.relation['children'].setdefault(child.metadata.identifier, child)

    def find_parent(self, *tag: str):
        p_table = set()

        def __parent_generator(parent: "InteractiveObject"):
            for _i, _p in parent.parents.items():
                if _i in p_table:
                    continue
                p_table.add(_i)
                yield _p
                if _p.parents:
                    yield from __parent_generator(_p)

        for p in __parent_generator(self):
            if p.compare(*tag):
                return p

    def find_child(self, *tag: str):
        c_table = set()

        def __child_generator(child: "InteractiveObject"):
            for _i, _c in child.children.items():
                if _i in c_table:
                    continue
                c_table.add(_i)
                yield _c
                if _c.children:
                    yield from __child_generator(_c)

        for c in __child_generator(self):
            if c.compare(*tag):
                return c

    @property
    def all_components(self):
        return self._components.values()

    def get_component(self, __t: Union[str, Type[TC]]) -> TC:
        if isinstance(__t, str):
            return self._components.get(__t)
        for __c in filter(lambda x: isinstance(x, __t), list(self._components.values())):
            return __c

    def get_components(self, __t: Type[TC]) -> List[TC]:
        result = []
        for __c in filter(lambda x: isinstance(x, __t), list(self._components.values())):
            result.append(__c)
        return result

    def get_component_in_parent(self, __t: Union[str, Type[TC]]) -> TC:
        for __i in self.relation['parents'].values():
            if __c := __i.get_component(__t):
                return __c

    def get_component_in_children(self, __t: Union[str, Type[TC]]) -> TC:
        for __i in self.relation['children'].values():
            if __c := __i.get_component(__t):
                return __c

    def action(self, method_name: str) -> Callable[..., Coroutine]:
        for func in [getattr(c, method_name, None) for c in self.all_components]:
            if not func:
                continue
            return func

    def __getattr__(self, item):
        if item in self.__ignore__:
            return self.__getattribute__(item)
        return self._components.get(item)

    def __setattr__(self, key, value: Union[Dict[str, Component], Component]):
        if key in self.__ignore__:
            super(InteractiveObject, self).__setattr__(key, value)
        else:
            self._components.setdefault(key, value)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}; "
            f"{', '.join([f'{k}={v}' for k, v in self._components.items()])}>"
        )

    def __getstate__(self):
        return {
            "metadata": {k: v for k, v in self.metadata.__dict__.items() if k not in ("io", "protocol")},
            "behavior": self.prefab_behavior
        }

    def __eq__(self, other: "InteractiveObject"):
        return self.__getstate__() == other.__getstate__()

    def __hash__(self):
        return hash(tuple(self.__getstate__().items()))

    def __class_getitem__(cls, item):
        cls.__check_tags__.append([item] if isinstance(item, str) else [*item])
        return cls
