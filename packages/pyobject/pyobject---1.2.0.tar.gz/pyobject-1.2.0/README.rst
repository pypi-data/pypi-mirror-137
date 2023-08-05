pyobject - 一个关于Python对象工具的模块。A tool of python object with tkinter and command-lines.

.. image:: https://tiebapic.baidu.com/forum/pic/item/4e4a20a4462309f707621658650e0cf3d7cad66f.jpg
    :alt: Build passing
.. image:: https://tiebapic.baidu.com/forum/pic/item/d1a20cf431adcbefc104ee4cbbaf2edda3cc9f4c.jpg
    :alt: 100% test coverage

所包含模块 Included modules: 
============================

__init__ - 打印出Python对象的各个属性

pyobject.browser - 以图形方式浏览Python对象

pyobject.code\_ - Python bytecode的操作工具

pyobject.search - 搜索python对象

pyobject.newtypes - 定义一些新的类型

包含的函数 Functions:
===========================
objectname(obj)::

    objectname(obj) - 返回一个对象的名称,形如xxmodule.xxclass。
    如:objectname(int) -> 'builtins.int'

bases(obj, level=0, tab=4)::

    bases(obj) - 打印出该对象的基类
    tab:缩进的空格数,默认为4。

describe(obj, level=0, maxlevel=1, tab=4, verbose=False, file=sys.stdout, mode='w' encoding='utf-8')::

    "描述"一个对象,即打印出对象的各个属性。
    参数说明:
    maxlevel:打印对象属性的层数。
    tab:缩进的空格数,默认为4。
    verbose:一个布尔值,是否打印出对象的特殊方法(如__init__)。
    file:一个类似文件的对象。


browse(object, verbose=False, name='obj')::

    以图形方式浏览一个Python对象。
    verbose:与describe相同,是否打印出对象的特殊方法(如__init__)

新增函数 New Functions:
=============================

make_list(start_obj, recursions=2, all=False)::

    创建一个对象的列表, 列表中无重复的对象。
    start:开始搜索的对象
    recursion:递归次数
    all:是否将对象的特殊属性(如__init__)加入列表

make_iter(start_obj, recursions=2, all=False)::

    功能、参数与make_list相同, 但创建迭代器, 且迭代器中可能有重复的对象。

search(obj, start, recursions=3)::

    从一个起点开始搜索对象
    obj:待搜索的对象
    start:起点对象
    recursion:递归次数

新增类: ``pyobject.newtypes.Code``
用法\: (下面的示例是从doctest中摘取的)::

    >>> def f():print("Hello")
    >>> c=Code.fromfunc(f)
    >>> c.co_consts
    (None, 'Hello')
    >>> c.co_consts=(None, 'Hello World!')
    >>> c.exec()
    Hello World!
    >>>
    >>> import os,pickle
    >>> temp=os.getenv('temp')
    >>> with open(os.path.join(temp,"temp.pkl"),'wb') as f:
    ...     pickle.dump(c,f)
    ... 
    >>> f=open(os.path.join(temp,"temp.pkl"),'rb')
    >>> pickle.load(f).to_func()()
    Hello World!
    >>> 
    >>> c.to_pycfile(os.path.join(temp,"temppyc.pyc"))
    >>> sys.path.append(temp)
    >>> import temppyc
    Hello World!
    >>> Code.from_pycfile(os.path.join(temp,"temppyc.pyc")).exec()
    Hello World!


版本:1.2.0

*最近更新: 2022-2-2*

改进:修复了一些bug,优化了search类的性能; pyobject.code_中增加了Code类,browser中增加编辑属性功能, 增加了Code类的测试。

源码:见 <https://github.com/qfcy/Python/tree/main/pyobject>`_

作者 Author:
*七分诚意 qq:3076711200 邮箱:3416445406@qq.com*

作者主页: <https://blog.csdn.net/qfcy\_/>`_