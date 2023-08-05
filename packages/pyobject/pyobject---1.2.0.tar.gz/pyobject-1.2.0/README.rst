pyobject - һ������Python���󹤾ߵ�ģ�顣A tool of python object with tkinter and command-lines.

.. image:: https://tiebapic.baidu.com/forum/pic/item/4e4a20a4462309f707621658650e0cf3d7cad66f.jpg
    :alt: Build passing
.. image:: https://tiebapic.baidu.com/forum/pic/item/d1a20cf431adcbefc104ee4cbbaf2edda3cc9f4c.jpg
    :alt: 100% test coverage

������ģ�� Included modules: 
============================

__init__ - ��ӡ��Python����ĸ�������

pyobject.browser - ��ͼ�η�ʽ���Python����

pyobject.code\_ - Python bytecode�Ĳ�������

pyobject.search - ����python����

pyobject.newtypes - ����һЩ�µ�����

�����ĺ��� Functions:
===========================
objectname(obj)::

    objectname(obj) - ����һ�����������,����xxmodule.xxclass��
    ��:objectname(int) -> 'builtins.int'

bases(obj, level=0, tab=4)::

    bases(obj) - ��ӡ���ö���Ļ���
    tab:�����Ŀո���,Ĭ��Ϊ4��

describe(obj, level=0, maxlevel=1, tab=4, verbose=False, file=sys.stdout, mode='w' encoding='utf-8')::

    "����"һ������,����ӡ������ĸ������ԡ�
    ����˵��:
    maxlevel:��ӡ�������ԵĲ�����
    tab:�����Ŀո���,Ĭ��Ϊ4��
    verbose:һ������ֵ,�Ƿ��ӡ����������ⷽ��(��__init__)��
    file:һ�������ļ��Ķ���


browse(object, verbose=False, name='obj')::

    ��ͼ�η�ʽ���һ��Python����
    verbose:��describe��ͬ,�Ƿ��ӡ����������ⷽ��(��__init__)

�������� New Functions:
=============================

make_list(start_obj, recursions=2, all=False)::

    ����һ��������б�, �б������ظ��Ķ���
    start:��ʼ�����Ķ���
    recursion:�ݹ����
    all:�Ƿ񽫶������������(��__init__)�����б�

make_iter(start_obj, recursions=2, all=False)::

    ���ܡ�������make_list��ͬ, ������������, �ҵ������п������ظ��Ķ���

search(obj, start, recursions=3)::

    ��һ����㿪ʼ��������
    obj:�������Ķ���
    start:������
    recursion:�ݹ����

������: ``pyobject.newtypes.Code``
�÷�\: (�����ʾ���Ǵ�doctest��ժȡ��)::

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


�汾:1.2.0

*�������: 2022-2-2*

�Ľ�:�޸���һЩbug,�Ż���search�������; pyobject.code_��������Code��,browser�����ӱ༭���Թ���, ������Code��Ĳ��ԡ�

Դ��:�� <https://github.com/qfcy/Python/tree/main/pyobject>`_

���� Author:
*�߷ֳ��� qq:3076711200 ����:3416445406@qq.com*

������ҳ: <https://blog.csdn.net/qfcy\_/>`_