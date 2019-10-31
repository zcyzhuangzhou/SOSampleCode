import os

from sekg.graph.factory import GraphInstanceFactory
from sekg.mysql.factory import MysqlSessionFactory

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

MYSQL_CONFIG_PATH = os.path.join(ROOT_DIR, 'mysql_config.json')
MYSQL_FACTORY = MysqlSessionFactory(MYSQL_CONFIG_PATH)

# the output dir
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
# the data dir
DATA_DIR = os.path.join(ROOT_DIR, 'data')
# the qualified_name dir
QUALIFIED_NAME_DIR = os.path.join(ROOT_DIR, 'qualified_name.json')

TRAIN_SAMPLE_CODE = os.path.join(DATA_DIR, 'train_test.json')

# the tf-idf dir
TFIDF_DIR = os.path.join(OUTPUT_DIR, 'tfidf')