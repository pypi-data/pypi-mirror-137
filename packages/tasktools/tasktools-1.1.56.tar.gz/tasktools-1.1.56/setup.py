from setuptools import setup, find_packages
from pathlib import Path

path = Path(__file__).resolve().parent
with open(path/'README.md', encoding='utf-8') as f:
    long_description = f.read()

with open(path/'VERSION') as version_file:
    version = version_file.read().strip()


setup(name='tasktools',
      version=version,
      description='Some useful tools for asycnio Tasks: async while, the Scheduler and Assignator classes',
      url='https://tasktools.readthedocs.io/en/latest/',
      author='David Pineda Osorio',
      author_email='dpineda@uchile.cl',
      license='GPLv3',
      install_requires=['networktools'],      
      package_dir={'tasktools': 'tasktools'},
      package_data={
          'tasktools': ['../doc', '../docs', '../requeriments.txt']},
      packages=find_packages(),
      include_package_data=True,
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
