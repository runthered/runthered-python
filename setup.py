from setuptools import setup, find_packages
import os

version = open('VERSION').read().strip()

setup(name='runthered_python',
      author='Finn Colman',
      author_email='finn.colman@runthered.com',
      maintainer='Run The Red',
      maintainer_email='support@runthered.com',
      version=version,
      description='Run The Red Python API wrapper library',
      long_description='Run The Red Python API wrapper library',
      license='MIT',
      url='http://www.runthered.com/',
      packages = find_packages(exclude=[
          'tests*', '_trial_temp'
           ]),
      classifiers=['Development Status :: 3 - Alpha',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
      ],
      keywords='runthered, rtr',
      zip_safe=False,
      data_files = []
      )
