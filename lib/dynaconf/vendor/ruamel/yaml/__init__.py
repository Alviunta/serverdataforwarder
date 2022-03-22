from __future__ import print_function,absolute_import,division,unicode_literals
_B='yaml'
_A=False
if _A:from typing import Dict,Any
_package_data=dict(full_package_name='ruamel.yaml',version_info=(0,16,10),__version__='0.16.10',author='Anthon van der Neut',author_email='a.van.der.neut@ruamel.eu',description='ruamel.yaml is a YAML parser/emitter that supports roundtrip preservation of comments, seq/map flow style, and map key order',entry_points=None,since=2014,extras_require={':platform_python_implementation=="CPython" and python_version<="2.7"':['ruamel.ordereddict'],':platform_python_implementation=="CPython" and python_version<"3.9"':['ruamel.yaml.clib>=0.1.2'],'jinja2':['ruamel.yaml.jinja2>=0.2'],'docs':['ryd']},classifiers=['Programming Language :: Python :: 2.7','Programming Language :: Python :: 3.5','Programming Language :: Python :: 3.6','Programming Language :: Python :: 3.7','Programming Language :: Python :: 3.8','Programming Language :: Python :: Implementation :: CPython','Programming Language :: Python :: Implementation :: PyPy','Programming Language :: Python :: Implementation :: Jython','Topic :: Software Development :: Libraries :: Python Modules','Topic :: Text Processing :: Markup','Typing :: Typed'],keywords='yaml 1.2 parser round-trip preserve quotes order config',read_the_docs=_B,supported=[(2,7),(3,5)],tox=dict(env='*',deps='ruamel.std.pathlib',fl8excl='_test/lib'),universal=True,rtfd=_B)
version_info=_package_data['version_info']
__version__=_package_data['__version__']
try:from .cyaml import *;__with_libyaml__=True
except (ImportError,ValueError):__with_libyaml__=_A
from dynaconf.vendor.ruamel.yaml.main import *