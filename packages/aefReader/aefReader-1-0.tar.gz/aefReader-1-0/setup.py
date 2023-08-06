from setuptools import setup

with open("README.md", "r") as ld:
    long_description = ld.read()

setup(name='aefReader',
      version='1с0',
      long_description=long_description,
      long_description_content_type="text/markdown",
      description='reading .aef files',
      packages=['aefReader'],
      author_email='4dcubeoff@gmail.com',
      zip_safe=False,
      author="Savtis")