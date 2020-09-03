from setuptools import setup

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

with open("README", 'r') as f:
    long_description = f.read()


setup(
   name='wordRecog',
   version='1.0',
   description='A small module to transcribe photos of handwritten text',
   license="MIT",
   long_description=long_description,
   author='Aidan Tweedy',
   author_email='atweedy1@binghamton.edu',
   packages=['wordRecog'],
   install_requires=REQUIREMENTS
)