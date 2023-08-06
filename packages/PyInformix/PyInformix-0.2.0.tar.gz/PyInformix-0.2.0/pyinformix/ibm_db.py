from __future__ import absolute_import
from __future__ import unicode_literals

from ibm_db_sa.base import CHAR, DATE, DATETIME, INTEGER, SMALLINT, BIGINT, DECIMAL, NUMERIC, REAL, VARCHAR, FLOAT, \
    compiler, default, ibm_reflection, sa_types, _SelectLastRowIDMixin as _SelectLastRowIDMixinBase, DB2Compiler, \
    DB2IdentifierPreparer, DB2Dialect

from sqlalchemy.exc import ArgumentError


RESERVED_WORDS = set([
    'a', 'abort', 'abs', 'absolute', 'access', 'acos', 'acquire', 'action', 'activate', 'ada', 'add', 'addform',
    'admin', 'after', 'aggregate', 'alias', 'all', 'allocate', 'alter', 'an', 'analyze', 'and', 'any', 'append',
    'archive', 'archivelog', 'are', 'array', 'arraylen', 'as', 'asc', 'ascii', 'asin', 'assertion', 'at', 'atan',
    'audit', 'authorization', 'avg', 'avgu', 'backup', 'become', 'before', 'begin', 'between', 'bigint', 'binary',
    'bind', 'binding', 'bit', 'blob', 'block', 'body', 'boolean', 'both', 'breadth', 'break', 'breakdisplay', 'browse',
    'bufferpool', 'bulk', 'by', 'byref', 'cache', 'call', 'callproc', 'cancel', 'capture', 'cascade', 'cascaded',
    'case', 'cast', 'catalog', 'ccsid', 'ceiling', 'change', 'char', 'character', 'chartorowid', 'check', 'class',
    'clob', 'checkpoint', 'chr', 'cleanup', 'clear', 'clearrow', 'close', 'cluster', 'clustered', 'coalesce', 'cobol',
    'colgroup', 'collate', 'collation', 'collection', 'column', 'command', 'comment', 'commit', 'completion',
    'committed', 'compile', 'complex', 'compress', 'compute', 'concat', 'confirm', 'connect', 'connection',
    'constraint', 'constraints', 'constructor', 'contains', 'containstable', 'contents', 'continue', 'controlfile',
    'controlrow', 'convert', 'copy', 'corresponding', 'cos', 'count', 'countu', 'crcols', 'create', 'cross', 'cube',
    'current', 'current_date', 'current_path', 'current_role', 'current_time', 'current_timestamp', 'current_user',
    'cursor', 'cvar', 'cycle', 'data', 'database', 'datafile', 'datahandler', 'datapages', 'date', 'day', 'dayofmonth',
    'dayofweek', 'dayofyear', 'days', 'dba', 'dbcc', 'dbspace', 'deallocate', 'dec', 'decimal', 'declaration',
    'declare', 'decode', 'default', 'deferrable', 'deferred', 'define', 'definition', 'degrees', 'delete', 'depth',
    'deref', 'deleterow', 'deny', 'desc', 'describe', 'descriptor', 'destroy', 'dhtype', 'destructor', 'deterministic',
    'dictionary', 'diagnostics', 'direct', 'disable', 'disabled', 'disconnect', 'disk', 'dismount', 'display',
    'distinct', 'distribute', 'distributed', 'do', 'domain', 'double', 'down', 'drop', 'dummy', 'dump', 'dynamic',
    'each', 'editproc', 'else', 'elseif', 'enable', 'end', 'enddata', 'enddisplay', 'endexec', 'end-exec', 'endforms',
    'endif', 'endloop', 'equals', 'endselect', 'endwhile', 'erase', 'errlvl', 'errorexit', 'escape', 'events', 'every',
    'except', 'exception', 'exceptions', 'exclude', 'excluding', 'exclusive', 'exec', 'execute', 'exists', 'exit',
    'exp', 'explain', 'explicit', 'expression', 'extent', 'external', 'externally', 'extract', 'false', 'fetch',
    'field', 'fieldproc', 'file', 'fillfactor', 'filtering', 'finalize', 'finalize', 'first', 'float', 'floor',
    'floppy', 'flush', 'for', 'force', 'formdata', 'forminit', 'forms', 'fortran', 'foreign', 'found ', 'fragment',
    'freelist', 'freelists', 'freetext', 'freetexttable', 'from', 'free', 'full', 'function', 'general', 'get',
    'getcurrentconnection', 'getform', 'getoper', 'getrow', 'global', 'go', 'goto', 'grant', 'granted', 'graphic',
    'greatest', 'group', 'grouping', 'groups', 'hash', 'having', 'host', 'help', 'helpfile', 'holdlock', 'hour',
    'hours', 'identified', 'identity', 'ignore', 'identitycol', 'if', 'ifnull', 'iimessage', 'iiprintf', 'immediate',
    'import', 'in', 'include', 'including', 'increment', 'index', 'indexpages', 'indicator', 'initcap', 'initial',
    'initialize', 'initially', 'initrans', 'inittable', 'inner', 'inout', 'input', 'insensitive', 'insert', 'insertrow',
    'instance', 'instr', 'int', 'integer', 'integrity', 'interface', 'intersect', 'interval', 'into', 'is', 'isolation',
    'iterate', 'join', 'key', 'kill', 'label', 'language', 'large', 'last', 'lateral', 'layer', 'leading', 'least',
    'left', 'less', 'length', 'level', 'like', 'limit', 'lineno', 'link', 'list', 'lists', 'load', 'loadtable', 'local',
    'localtime', 'localtimestamp', 'locator', 'locate', 'lock', 'locksize', 'log', 'logfile', 'long', 'longint',
    'lower', 'lpad', 'ltrim', 'lvarbinary', 'lvarchar', 'main', 'manage', 'manual', 'map', 'match', 'max',
    'maxdatafiles', 'maxextents', 'maxinstances', 'maxlogfiles', 'maxloghistory', 'maxlogmembers', 'maxtrans',
    'maxvalue', 'menuitem', 'message', 'microsecond', 'microseconds', 'min', 'minextents', 'minus', 'minute',
    'modifies', 'minutes', 'minvalue', 'mirrorexit', 'mod', 'mode', 'modify', 'module', 'money', 'month', 'months',
    'mount', 'move', 'name', 'named', 'names', 'national', 'natural', 'nchar', 'nclob', 'new', 'next', 'nheader', 'no',
    'noarchivelog', 'noaudit', 'nocache', 'nocheck', 'nocompress', 'nocycle', 'noecho', 'nomaxvalue', 'nominvalue',
    'nonclustered', 'none', 'noorder', 'noresetlogs', 'normal', 'nosort', 'not', 'notfound', 'notrim', 'nowait', 'null',
    'nullif', 'nullvalue', 'number', 'numeric', 'object', 'numparts', 'nvl', 'obid', 'odbcinfo', 'of', 'off', 'offline',
    'offsets', 'old', 'on', 'once', 'online', 'only', 'open', 'operation', 'opendatasource', 'openquery', 'openrowset',
    'optimal', 'optimize', 'option', 'or', 'order', 'ordinality', 'out', 'outer', 'output', 'over', 'overlaps', 'own',
    'package', 'pad', 'parameter', 'parameters', 'page', 'pages', 'parallel', 'part', 'partial', 'path', 'postfix',
    'pascal', 'pctfree', 'pctincrease', 'pctindex', 'pctused', 'percent', 'perm', 'permanent', 'permit', 'pi', 'pipe',
    'plan', 'pli', 'position', 'power', 'precision', 'prefix', 'preorder', 'prepare', 'preserve', 'primary', 'print',
    'printscreen', 'prior', 'priqty', 'private', 'privileges', 'proc', 'procedure', 'processexit', 'profile', 'program',
    'prompt', 'public', 'putform', 'putoper', 'putrow', 'qualification', 'quarter', 'quota', 'radians', 'raise',
    'raiserror', 'rand', 'range', 'raw', 'read', 'reads', 'readtext', 'real', 'recursive', 'ref', 'reconfigure',
    'record', 'recover', 'redisplay', 'references', 'referencing', 'relative', 'register', 'release', 'relocate ',
    'remainder', 'remove', 'rename', 'repeat', 'repeatable', 'repeated', 'replace', 'replicate', 'replication', 'reset',
    'resetlogs', 'resource', 'restore', 'restrict', 'result', 'restricted', 'resume', 'retrieve', 'return', 'returns',
    'reuse', 'revoke', 'right', 'role', 'roles', 'rollback', 'rollup', 'routine', 'row', 'rows', 'rowcount',
    'rowguidcol', 'rowid', 'rowids', 'rowidtochar', 'rowlabel', 'rownum', 'rows', 'rpad', 'rrn', 'rtrim', 'rule', 'run',
    'runtimestatistics', 'save', 'savepoint', 'schedule', 'schema', 'scn', 'screen', 'scroll', 'scope', 'search',
    'scrolldown', 'scrollup', 'second', 'seconds', 'secqty', 'section', 'segment', 'select', 'sequence', 'serializable',
    'service', 'session', 'session_user', 'set', 'sets', 'setuser', 'sin', 'simple', 'sign', 'shutdown', 'short',
    'share', 'shared', 'setuser', 'size', 'sleep', 'smallint', 'snapshot', 'some', 'sort', 'soundex', 'space',
    'specific', 'specifictype', 'sql', 'sqlexception', 'sqlbuf', 'sqlca', 'sqlcode', 'sqlerror', 'sqlstate',
    'sqlwarning', 'sqrt', 'start', 'state', 'statement', 'static', 'structure', 'statistics', 'stogroup', 'stop',
    'storage', 'storpool', 'submenu', 'subpages', 'substr', 'substring', 'successful', 'suffix', 'sum', 'system_user',
    'sumu', 'switch', 'synonym', 'syscat', 'sysdate', 'sysfun', 'sysibm', 'sysstat', 'system', 'systime',
    'systimestamp', 'table', 'tabledata', 'tables', 'tablespace', 'tan', 'tape', 'temp', 'temporary', 'terminate',
    'than', 'textsize', 'then', 'thread', 'time', 'timeout', 'timestamp', 'timezone_hour', 'timezone_minute', 'tinyint',
    'to', 'top', 'tpe', 'tracing', 'trailing', 'tran', 'transaction', 'translate', 'translation', 'treat', 'trigger',
    'triggers', 'trim', 'true', 'truncate', 'tsequal', 'type', 'uid', 'uncommitted', 'under', 'union', 'unique',
    'unknown', 'unnest', 'unlimited', 'unloadtable', 'unsigned', 'until', 'up', 'update', 'updatetext', 'upper',
    'usage', 'use', 'user', 'using', 'uuid', 'validate', 'validproc', 'validrow', 'value', 'values', 'varbinary',
    'varchar', 'variable', 'variables', 'varying', 'vcat', 'version', 'vercols', 'view', 'volumes', 'waitfor', 'week',
    'when', 'whenever', 'where', 'while', 'with', 'without', 'work', 'write', 'writetext', 'year', 'years', 'zone'
])


class BIGSERIAL(sa_types.BIGINT):
    __visit_name__ = 'BIGSERIAL'


class BSON(sa_types.BINARY):
    __visit_name__ = 'BSON'


class BYTE(sa_types.BLOB):
    __visit_name__ = 'BYTE'


class INTERVAL(sa_types.Interval):
    __visit_name__ = 'INTERVAL'


class JSON(sa_types.JSON):
    __visit_name__ = 'JSON'


class MONEY(sa_types.DECIMAL):
    __visit_name__ = 'MONEY'


class NCHAR(sa_types.NCHAR):
    __visit_name__ = 'NCHAR'


class NVARCHAR(sa_types.NVARCHAR):
    __visit_name__ = 'NVARCHAR'


class SERIAL(sa_types.INT):
    __visit_name__ = 'SERIAL'


class SMALLFLOAT(sa_types.FLOAT):
    __visit_name__ = 'SMALLFLOAT'


class TEXT(sa_types.TEXT):
    __visit_name__ = 'TEXT'


ischema_names = {
    'BIGINT': BIGINT,
    'BIGSERIAL': BIGSERIAL,
    'BSON': BSON,
    'BYTE': BYTE,
    'CHAR': CHAR,
    'CHARACTER': CHAR,
    'CHARACTER VARYING': VARCHAR,
    'DATE': DATE,
    'DATETIME': DATETIME,
    'DEC': DECIMAL,
    'DECIMAL': DECIMAL,
    'DOUBLE PRECISION': FLOAT,
    'FLOAT': FLOAT,
    'INT': INTEGER,
    'INT8': BIGINT,
    'INTEGER': INTEGER,
    'INTERVAL': INTERVAL,
    'JSON': JSON,
    'MONEY': MONEY,
    'NCHAR': NCHAR,
    'NUMERIC': NUMERIC,
    'NVARCHAR': NVARCHAR,
    'REAL': REAL,
    'SERIAL': SERIAL,
    'SERIAL8': BIGSERIAL,
    'SMALLFLOAT': SMALLFLOAT,
    'SMALLINT': SMALLINT,
    'TEXT': TEXT,
    'VARCHAR': VARCHAR
}


class InformixReflector(ibm_reflection.DB2Reflector):
    def _get_default_schema_name(self, connection):
        return None


class InformixTypeCompiler(compiler.GenericTypeCompiler):
    def visit_BIGSERIAL(self, type_):
        return 'BIGSERIAL'

    def visit_BSON(self, type_):
        return 'BSON'

    def visit_BYTE(self, type_):
        return 'BYTE'

    def visit_CHAR(self, type_, **kw):
        return 'CHAR' if type_.length in (None, 0) else 'CHAR(%(length)s)' % {'length': type_.length}

    def visit_INTERVAL(self, type_):
        return 'INTERVAL'

    def visit_JSON(self, type_):
        return 'JSON'

    def visit_MONEY(self, type_):
        if not type_.precision:
            return 'MONEY(31, 0)'
        elif not type_.scale:
            return 'MONEY(%(precision)s, 0)' % {'precision': type_.precision}
        else:
            return 'MONEY(%(precision)s, %(scale)s)' % {'precision': type_.precision, 'scale': type_.scale}

    def visit_NCHAR(self, type_, **kw):
        return 'NCHAR' if type_.length in (None, 0) else 'NCHAR(%(length)s)' % {'length': type_.length}

    def visit_NVARCHAR(self, type_, **kw):
        return 'NVARCHAR(%(length)s)' % {'length': type_.length}

    def visit_SERIAL(self, type_):
        return 'SERIAL' if type_.length is None else 'SERIAL(%(length)s)' % {'length': type_.length}

    def visit_SMALLFLOAT(self, type_):
        return 'SMALLFLOAT'

    def visit_VARCHAR(self, type_, **kw):
        return 'VARCHAR(%(length)s)' % {'length': type_.length}


class InformixCompiler(DB2Compiler):
    def default_from(self):
        # Informix uses sysmaster:"informix".sysdual table for row count
        return ' FROM sysmaster:"informix".sysdual'


class InformixIdentifierPreparer(DB2IdentifierPreparer):
    reserved_words = RESERVED_WORDS
    illegal_initial_characters = set(range(0, 10)).union(["_", "$"])


class _SelectLastRowIDMixin(_SelectLastRowIDMixinBase):
    def post_exec(self):
        self._lastrowid = None


class InformixExecutionContext(_SelectLastRowIDMixin, default.DefaultExecutionContext):
    def fire_sequence(self, seq, type_):
        return default.arg


class InformixDialect(DB2Dialect):
    driver = 'ifx'
    supports_statement_cache = False

    ischema_names = ischema_names

    statement_compiler = InformixCompiler
    type_compiler = InformixTypeCompiler
    preparer = InformixIdentifierPreparer
    execution_ctx_cls = InformixExecutionContext

    _reflector_cls = InformixReflector

    _isolation_lookup = set([
        'DIRTY READ',
        'COMMITTED READ',
        'REPEATABLE READ'
    ])

    @classmethod
    def dbapi(cls):
        """ Returns: the underlying DBAPI driver module
        """
        import ibm_db_dbi as module
        return module

    def create_connect_args(self, url):
        dsn = 'SERVICE=%s' % url.port

        kwargs = {}

        kwargs.update(url.query)

        return ((dsn, url.username, url.password, url.host, url.database), kwargs)

    def set_isolation_level(self, connection, level):
        if level is None:
            level = self.default_isolation_level
        else:
            if len(level.strip()) < 1:
                level = self.default_isolation_level

        level.upper().replace('-', ' ')

        if level not in self._isolation_lookup:
            raise ArgumentError(
                "Invalid value '%s' for isolation_level. "
                "Valid isolation levels for %s are %s" %
                (level, self.driver, ', '.join(self._isolation_lookup))
            )

        cursor = connection.cursor()

        try:
            cursor.execute('SET ISOLATION %s' % level)
            cursor.execute('COMMIT')
        finally:
            cursor.close()

    def get_isolation_level(self, connection):
        cursor = connection.cursor()

        try:
            cursor.execute('SELECT F.txt FROM sysmaster:"informix".sysrstcb R JOIN sysmaster:"informix".systxptab T ON R.txp = T.address JOIN sysmaster:"informix".flags_text F ON (T.isolevel = F.flags AND F.tabname = \'sysopendb\') WHERE R.sid = DBINFO(\'sessionid\')')

            level = cursor.fetchone()[0]
        finally:
            cursor.close()

        return level

    def initialize(self, connection):
        connection.connection.dbms_name = 'DB2'

        super(InformixDialect, self).initialize(connection)

        _reflector_cls = InformixReflector

        self._reflector = _reflector_cls(self)


# legacy naming
IBM_DBCompiler = InformixCompiler
IBM_DBIdentifierPreparer = InformixIdentifierPreparer
IBM_DBExecutionContext = InformixExecutionContext
IBM_DBDialect = InformixDialect

dialect = InformixDialect
