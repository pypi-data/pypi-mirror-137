from sqlalchemy import util
from sqlalchemy.sql import sqltypes

from sqlalchemy_jdbcapi.base import MixedBinary, BaseDialect

from .ibm_db import InformixDialect

colspecs = util.update_copy(
    InformixDialect.colspecs, {sqltypes.LargeBinary: MixedBinary},
)


class InformixJDBCDialect(BaseDialect, InformixDialect):
    driver = 'ifx_jdbc'
    supports_statement_cache = False

    jdbc_db_name = 'informix-sqli'
    jdbc_driver_name = 'com.informix.jdbc.IfxDriver'
    colspecs = colspecs

    def create_connect_args(self, url):
        if url is None:
            return

        # dialects expect jdbc url e.g.
        # "jdbc:informix-sqli://{hostname}:{port}/{database};INFORMIXSERVER={server};user={username};password={password}"
        # if sqlalchemy create_engine() url is passed e.g.
        # "informix://{username}:{password}@{hostname}/{database}"
        # it is parsed wrong
        # restore original url
        s: str = str(url)
        # get jdbc url
        jdbc_url: str = s.split('//', 1)[-1]

        # add driver information
        if not jdbc_url.startswith('jdbc'):
            jdbc_url = f"jdbc:{self.jdbc_db_name}://{jdbc_url}"

        kwargs = {
            'jclassname': self.jdbc_driver_name,
            'url': jdbc_url,
            # pass driver args via JVM System settings
            'driver_args': []
        }

        return ((), kwargs)
