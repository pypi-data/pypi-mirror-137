#!/usr/bin/env python

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='vertica_locust_client',
      version='0.0.2',
      description='A Vertica client for use with the locust.io load testing tool',
      long_description=readme(),
      author='Matt Spilchen',
      author_email='matt.spilchen@vertica.com',
      license="Apache License, Version 2.0",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3',
      ],
      python_requires='>=3',
      zip_safe=False,
      install_requires=['vertica-python==1.0.3',
                        'locust==2.7.3',
                        'carbon-client==0.3.3'],
)
