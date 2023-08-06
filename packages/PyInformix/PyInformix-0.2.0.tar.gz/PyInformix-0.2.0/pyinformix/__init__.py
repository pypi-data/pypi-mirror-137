from sqlalchemy.dialects import registry

__version__ = '0.2.0'

registry.register('informix', 'pyinformix.ibm_db', 'InformixDialect')
registry.register('informix.ibm_db', 'pyinformix.ibm_db', 'InformixDialect')
registry.register('informix.ifx_jdbc', 'pyinformix.ifx_jdbc', 'InformixJDBCDialect')
