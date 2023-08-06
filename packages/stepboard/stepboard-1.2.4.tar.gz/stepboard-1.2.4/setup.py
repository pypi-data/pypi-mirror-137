from setuptools import setup, find_packages

VERSION = '1.2.4'

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(name="stepboard",
      version=VERSION,
      author='Stępującybrat#1017',
      author_email='maciejwisniewski.ja@gmail.com',
      license='MIT',
      description='A simple library for making a dashboard in a flask/django.',
      packages=find_packages(),
      install_requires=['']
      )
