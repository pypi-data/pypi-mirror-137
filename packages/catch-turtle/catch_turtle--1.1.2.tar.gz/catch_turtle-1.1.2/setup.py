import catch_turtle,os,warnings
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

try:import turtle
except ImportError:
    warnings.warn("缺少turtle模块。 Module turtle required")

try:
    long_desc=open("README.rst").read()
except OSError:
    long_desc=catch_turtle.__doc__

setup(
  name='catch_turtle',
  version=catch_turtle.__version__,
  description="使用turtle模块制作的一款游戏。A game that made by using the *turtle* module.作者:七分诚意",
  long_description=long_desc,
  author=catch_turtle.__author__,#作者
  author_email=catch_turtle.__email__,
  url='https://github.com/qfcy/Python/tree/main/catch_turtle',
  packages=['catch_turtle'], #这里是所有代码所在的文件夹名称
  keywords=["python","turtle","game"],
  classifiers=["Topic :: Games/Entertainment",
               "Programming Language :: Python :: 3",
               "Natural Language :: Chinese (Simplified)",
               "Topic :: Education"]
)
