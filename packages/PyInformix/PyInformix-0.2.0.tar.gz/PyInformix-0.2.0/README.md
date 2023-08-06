# PyInformix

Experimental SQLAlchemy dialect for IBM Informix

## Installation

```
pip install PyInformix
```

## Usage

### Connect via ODBC*

```python
from sqlalchemy.engine import create_engine

engine = create_engine('informix+ibm_db://{username}:{password}@{hostname}:{port}/{database}')
```

*Requires [IBM Data Server Driver for ODBC and CLI software](https://www.ibm.com/docs/en/db2/11.1?topic=drivers-obtaining-data-server-driver-odbc-cli-software).

### Connect via JDBC*

```python
from sqlalchemy.engine import create_engine

engine = create_engine('informix+ifx_jdbc://{hostname}:{port}/{database};INFORMIXSERVER={server};delimident=y;user={username};password={password}')
```

Export CLASSPATH environment variable:

```
CLASSPATH=/path/to/informix_jdbc_x_x_x_x/jdbc-x.x.x.x.jar:/path/to/informix_jdbc_x_x_x_x/bson-x.x.x.jar
```

*Requires [IBM Informix JDBC Driver](http://www.ibm.com/software/data/informix/tools/jdbc) and [Java Runtime Environment (JRE)](https://www.java.com/en/download/).

## License

Distributed under the [Apache, version 2.0 license](https://opensource.org/licenses/Apache-2.0).