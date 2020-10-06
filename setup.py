from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='rubik',
   version='1.0',
   description='A useful module',
   license="MIT",
   long_description=long_description,
   author='Man Foo',
   author_email='foomail@foo.com',
   url="http://www.foopackage.com/",
   packages=['src'],  #same as name
   install_requires=['pandas', 'argparse', 'tqdm', 'numpy'], #external packages as dependencies
)
