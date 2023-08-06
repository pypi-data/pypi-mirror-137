from setuptools import setup, find_packages

setup(
    name='packageSatel',
    version='0.3',
    license='MIT',
    description='test package',
    long_description=open('README.md').read(),
    author='Juan Dombald',
    packages=find_packages(),
    install_requires=['json','statistics','collections','pandas','pydoc','pandas.io.json'],
    url='https://github.com/juanedomb/SATELLOGICTEST',

)