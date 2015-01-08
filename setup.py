# -*- coding: utf-8 -*- 
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
print(" setup.py is executed.....\n")
#print("here is pointing to:%r'%here)
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'pyramid_mako',
    'docutils',
    ]

setup(name='familymemo',
      version='0.0',
      description='familymemo',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='familymemo',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = familymemo:main
      [console_scripts]
      initialize_familymemo_db = familymemo.scripts.initializedb:main
      """,
      )
