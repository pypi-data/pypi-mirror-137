from setuptools import setup, find_packages

install_requires = [
    'requests',
    'contextlib2',
    'polling2',
    'urllib3',
    'multipledispatch',
    'mock',
    ]

setup(name='kingjimin',
version='2.1.19',
description='Test Package',
author='jiminlee',
author_email='jimin.lee@nota.ai',
install_requires=install_requires,
python_requires='>=3',
packages=find_packages()
)