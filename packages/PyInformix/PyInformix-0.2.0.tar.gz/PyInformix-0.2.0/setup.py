import os
import re

from setuptools import setup

with open(
    os.path.join(os.path.dirname(__file__), 'pyinformix', '__init__.py')
) as v_file:
    VERSION = (
        re.compile(r""".*__version__ = ["']([^\n]*)['"]""", re.S)
        .match(v_file.read())
        .group(1)
    )

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as r_file:
    readme = r_file.read()

setup(name='PyInformix',
      version=VERSION,
      description='Experimental SQLAlchemy dialect for IBM Informix',
      long_description_content_type='text/markdown',
      long_description=readme,
      license='Apache 2.0',
      url='https://github.com/homedepot/pyinformix',
      author='Mike Phillipson',
      author_email='MICHAEL_PHILLIPSON1@homedepot.com',
      packages=[
          'pyinformix'
      ],
      install_requires=[
          'ibm-db-sa',
          'sqlalchemy-jdbcapi'
      ],
      entry_points={
          'sqlalchemy.dialects': [
              'informix = pyinformix.ibm_db:InformixDialect',
              'informix.ibm_db = pyinformix.ibm_db:InformixDialect',
              'informix.ifx_jdbc = pyinformix.ifx_jdbc:InformixJDBCDialect'
          ]
      },
      zip_safe=False)
