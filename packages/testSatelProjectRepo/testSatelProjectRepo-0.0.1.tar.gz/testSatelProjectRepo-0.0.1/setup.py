from setuptools import setup, find_packages 


setup(
    name='testSatelProjectRepo',
    version='0.0.1',
    license='MIT',
    description='testing first package Satel stats',
    long_description=open('README.md').read(),
    author='Juan Dombald',
    packages=find_packages(),
    intall_requires=['urllib.request','json','statistics','collections','pandas','pydoc','pandas.io.json'],
    url='https://github.com/juanedomb/testSatelProjectRepo',
    
)