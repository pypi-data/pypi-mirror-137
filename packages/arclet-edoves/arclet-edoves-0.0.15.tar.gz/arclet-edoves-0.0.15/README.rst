Edoves
=========================
*las su dres rin romilu, nann sune ri edar neru.*



简介
----

|Licence| |PyPI| |PyPI - Python Version|

Edoves 是 ``Arclet Project`` 基于同项目下的 ``Cesloi``\ 的 **第二代**
框架实现,

**该框架目前处于快速迭代状态, API 可能会发生 剧烈 变化,
可能还不适合进行生产性的开发与运维**

特性
----

-  主要部分

   -  ☒ ``InteractiveObject``:
      对\ ``Unity3d``\ 中\ ``GameObject``\ 的简易模仿

      -  ☒ ``Monomer``: 代表逻辑关系的IO
      -  ☒ ``Module``: 负责处理事件的IO

         -  ☒ ``ServerDocker``: 负责网络会话交互
         -  ☒ ``Commander``: 基于 ``Arclet Alconna`` 的指令触发系统

   -  ☒ ``Component``: IO的主要属性, 负责实际的数据管理与事件响应
   -  ☒ ``Medium``: 传输事件信息的载体
   -  ☒ ``Protocol``: 调度\ ``Medium``\ 与\ ``IO``
   -  ☒ ``Scene``: 对IO统一的生命周期管理

-  实现支持

   -  ☒ ``Edoves for mirai-api-http`` : 对
      ```mirai-api-http`` <https://github.com/project-mirai/mirai-api-http>`__
      的支持.
   -  ☐ ``Edoves for OneBot`` : 对
      ```OneBot`` <https://github.com/botuniverse/onebot>`__ 的协议实现.
   -  ☐ ``Edoves for go-cqhttp`` : 对
      ```go-cqhttp`` <https://github.com/Mrs4s/go-cqhttp>`__ 的扩展 API
      支持.

样例
----

main.py:

.. code:: python

   from arclet.edoves.builtin.mah.actions import Reply
   from arclet.edoves.builtin.mah.module import MessageModule
   from arclet.edoves.builtin.medium import Message
   from arclet.edoves.builtin.event.message import AllMessage
   from arclet.edoves.builtin.client import AioHttpClient
   from arclet.edoves.main import Edoves


   async def test_message_reaction(message: Message):
       if message.content.startswith("Hello World"):
           await Reply(message).execute()
           await message.set("I received 'Hello World'!").send()


   app = Edoves(
       debug=False,
       profile={
           "verify_token": "INITKEYWylsVdbr",
           "port": "9080",
           "client": AioHttpClient,
           "account": 3542928737
       }
   )
   message_module = app.scene.activate_module(MessageModule)
   message_module.new_handler(AllMessage, test_message_reaction)
   app.run()

edoves/builtin/mah/module.py:

.. code:: python

   from arclet.edoves.main.module import BaseModule, ModuleMetaComponent
   from arclet.edoves.builtin.mah import VERIFY_CODE


   class MessageModuleData(ModuleMetaComponent):
       identifier = VERIFY_CODE


   class MessageModule(BaseModule):
       prefab_metadata = MessageModuleData

相关项目
--------

   这些项目都非常优秀, 我相信你听说过他们

-  ```Graia Framework`` <https://github.com/GraiaProject>`__

   -  ```Avilla`` <https://github.com/GraiaProject/Avilla>`__:
      ``Graia Project`` 的 “下一代” 框架实现
   -  ```Ariadne`` <https://github.com/GraiaProject/Ariadne>`__: 继承了
      ``Graia Project`` 中 ``Application`` 并进行了许多改进后产生的作品

-  ```Mamoe Technologies`` <https://github.com/mamoe>`__:

   -  ```mirai`` <https://github.com/mamoe/mirai>`__
   -  ```mirai-api-http`` <https://github.com/project-mirai/mirai-api-http>`__

开源协议
--------

Edoves 及其拓展 使用 MIT 作为开源协议.

但如果你若引用到了使用具有传染性开源协议（如 GPL/AGPL/LGPL 等）的项目,
请遵循相关规则.

.. |Licence| image:: https://img.shields.io/github/license/ArcletProject/Edoves
   :target: https://github.com/ArcletProject/Edoves/blob/main/LICENSE
.. |PyPI| image:: https://img.shields.io/pypi/v/arclet-edoves
   :target: https://pypi.org/project/arclet-edoves
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/arclet-edoves
   :target: https://www.python.org/
