import os
import re

from setuptools import setup

with open(
    os.path.join(os.path.dirname(__file__), 'flask_apialchemy', '__init__.py')
) as v_file:
    VERSION = (
        re.compile(r""".*__version__ = ["']([^\n]*)['"]""", re.S)
        .match(v_file.read())
        .group(1)
    )

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as r_file:
    readme = r_file.read()

setup(name='Flask-APIAlchemy',
      version=VERSION,
      description='Adds APIAlchemy support to your Flask application, modeled after Flask-SQLAlchemy.',
      long_description=readme,
      long_description_content_type='text/markdown',
      license='BSD-3-Clause',
      url='https://github.com/homedepot/flask-apialchemy',
      author='Mike Phillipson',
      author_email='MICHAEL_PHILLIPSON1@homedepot.com',
      packages=[
          'flask_apialchemy'
      ],
      install_requires=[
          'APIAlchemy',
          'Flask>=1.0.2,<2.0.0',
      ],
      tests_require=[
          'pytest'
      ],
      zip_safe=False)
