import os
import pathlib

# there should be a folder with the host file and the credentials path
try:
    config_folder = pathlib.Path(os.environ["SNOWFINCH_CONFIG"])
except KeyError:
    config_folder = pathlib.Path.home() / ".snowfinch"

# create folder
try:
    config_folder.mkdir(parents=True)
except OSError:
    pass

HOST_PATH = config_folder / ".hosts.json"
CREDENTIAL_PATH = config_folder / ".configs.json"

# the cryptography key can be in the same folder or at a separate location
try:
    KEY_PATH = os.environ["SNOWFINCH_KEY"]
except KeyError:
    KEY_PATH = config_folder / ".configkey"

STMT_START_KW = ['database ', 'drop ', 'create ', 'insert ', 'delete ', 'update ', 'merge ', '/*']
STMT_END_KW = ";"
STMT_SKIP_KW = ['error handling','#''collect stats proc',
                'call', '.if', '.run','lo comments end',
                'lo comments start','.export', '.quit',
                '.label', '.exit', '.set', '.run', '.logon',
                'bteq', 'set query band', 'select session',
                'call', 'sel sum(currentspool)', '.goto', 'fi',
                'rc', 'if', 'else', 'echo', 'exec', 'rm ',
                'cat', 'then', 'elif', 'exit', 'eof',
                '. $code', '#', 'awk ', 'sed ', '(echo'
                '/gpfs03', '${code}', 'export',
                ]

STG_SCHEMA_PRFX_LIST = ['WORK_', 'WRK_', 'TEMP_', 'TMP_', 'RZ_', 'VTT_', 'VT_', 'GTT', 'BLNCG', "_VT", "_VTT"]
QA_SCHEMA_PRFX_LIST = ['_LOAD_LOG', '_CNTRL']

# database flavors
DB_FLAVORS = (
    'postgresql',
    'mysql',
    'mssql',
    'teradata',
    'snowflake',
    'redshift',)

CACHE_SIZE = 64
CHUNK_SIZE = 30000
