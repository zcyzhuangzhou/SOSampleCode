import os

from sekg.graph.factory import GraphInstanceFactory
from sekg.mysql.factory import MysqlSessionFactory

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

NEO4J_CONFIG_PATH = os.path.join(ROOT_DIR, 'neo4j_config.json')
GRAPH_FACTORY = GraphInstanceFactory(NEO4J_CONFIG_PATH)

MYSQL_CONFIG_PATH = os.path.join(ROOT_DIR, 'mysql_config.json')
MYSQL_FACTORY = MysqlSessionFactory(MYSQL_CONFIG_PATH)

# the output dir
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
# the data dir
DATA_DIR = os.path.join(ROOT_DIR, 'data')
# the qualified_name dir
QUALIFIED_NAME_DIR = os.path.join(ROOT_DIR, 'qualified_name.json')

TRAIN_SAMPLE_CODE = os.path.join(DATA_DIR, 'train_test.json')
REMOVE_DUPLICATE_SAMPLE_CODE = os.path.join(OUTPUT_DIR, 'RemoveDuplicateSampleCode.json')
# the tf-idf dir
TFIDF_DIR = os.path.join(OUTPUT_DIR, 'tfidf')

GRAPH_DATA_DIR = os.path.join(OUTPUT_DIR, 'graph')
