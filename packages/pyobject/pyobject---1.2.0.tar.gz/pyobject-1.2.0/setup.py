import pyobject,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

try:
    long_desc=open("README.rst").read()
except OSError:
    long_desc=pyobject.__doc__

setup(
  name='pyobject',
  version=pyobject.__version__,
  description=pyobject.__doc__.replace('\n',''),
  long_description=long_desc,
  author=pyobject.__author__,
  author_email=pyobject.__email__,
  packages=['pyobject'],
  keywords=["pyobject","python","object","util","对象","bytecode"],
  classifiers=[
      'Programming Language :: Python',
      "Natural Language :: Chinese (Simplified)",
      "Topic :: Utilities",
      "Topic :: Software Development :: Libraries :: Python Modules"],
)
