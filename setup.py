# -*- coding: utf-8 -*-

from setuptools import setup

try:
  with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")
except:
  long_descr = "Will recursively search and validate the HTTP response code of each link on a specified web page - \
                and those of its children up - to the maximum specified recursion depth."
  
setup(name='link_validator',
      version='0.2.3',
      description='Recursive link validator',
      long_description=long_descr,
      url='http://github.com/at1as/link-validator',
      author='Jason Willems',
      author_email='hello@jasonwillems.com',
      license='MIT',
      packages=['link_validator'],
      entry_points = {
        "console_scripts": ['link_validator = link_validator.link_validator:main']
      },
      install_requires=[
        'argparse',
        'requests>=2.6.0',
        'beautifulsoup4',
        'termcolor'
      ],
      zip_safe=False)

