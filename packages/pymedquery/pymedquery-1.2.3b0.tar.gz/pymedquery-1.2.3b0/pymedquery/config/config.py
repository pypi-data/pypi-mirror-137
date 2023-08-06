import os
from collections import defaultdict
from typing import Dict, List, Tuple
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from pymedquery.src.helpers import nested_dict

# Paths
ROOT: str = os.getcwd()
SQL_PATH: str = os.path.join(ROOT, "pymedquery", "sql", "tables")
# Get the package path
data_path: str = pkg_resources.path('pymedquery.sql.default', 'image_default_query.sql')
sh_path: str = pkg_resources.path('pymedquery', 'medqueryInit.sh')
with data_path as sql, sh_path as sh:
    SERIES_MASK_QUERY_DEFAULT = str(sql)
    SHPATH = str(sh)

# postgres and storage params
DATABASE_TMP: str = 'medquery_template'

STORAGE_NAME: str = "medical_imaging_storage"
BUCKET_NAME: str = "multimodal-images"
bucket_dict: Dict[str, List[str]] = defaultdict(list)
blob_dict: Dict[str, List[str]] = defaultdict(list)
nested_blob_dict: Dict[str, Dict[str, any]] = nested_dict()
BUCKET_KEYS: List[str] = ["bucket_name", "creation_date"]

TEST_TABLE: str = 'junction_img_table'
PRIMARY_KEY: List[str] = ['study_uid']
NEW_COL_VALS: str = 'patient_333'
COL_TO_CHANGE: str = 'patient_uid'
COLS: List[str] = ['study_uid', 'patient_uid', 'exam_uid']
RECORDS: List[Tuple[str, str, str]] = [('project_king', 'patient_666', 'study_666')]
SQL_FILE_PATH: str = os.path.join(ROOT, 'pymedquery/data/sql/test.sql')
UPDATE_PRIMARY_KEY: str = 'project_king'

# Extensions
EXT_READTYPE_DICT: Dict[str, str] = {"pkl": "rb", "pickle": "r", "json": "r", "csv": "r", "gz": "rb"}

# Create tables config
create_dependencies: Dict[any, any] = {}
create_sql_command_dict: Dict[any, any] = {}

USER: str = os.environ.get('MQUSER')
PASSWORD: str = os.environ.get('MQPWD')
DATABASE: str = os.environ.get('DATABASE')
