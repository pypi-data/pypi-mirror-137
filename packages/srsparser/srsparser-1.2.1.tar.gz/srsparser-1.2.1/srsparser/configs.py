from os import getenv

from nltk import download, corpus
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# MongoDB database connection string
MONGODB_URL = getenv('MONGODB_URL')

# MongoDB database name
DB_NAME = getenv('DB_NAME')

# name of MongoDB collection with templates of software requirements specifications structures
TMPL_COLL_NAME = getenv('TMPL_COLL_NAME')

# name of MongoDB collection with parsing results
# (contains software requirements specifications structures filled according to the templates of the SRS structures)
RESULTS_COLL_NAME = getenv('RESULTS_COLL_NAME')

# regular expression for detection numbering elements
NUMBERING_PATTERN = '^([а-я0-9][.) ])+'

# minimal strings similarity ratio
MIN_SIMILARITY_RATIO = 0.5

download('stopwords', quiet=True)
STOPWORDS_RU = corpus.stopwords.words('russian')

SPECIAL_CHARS = "!#$%&'()*+,/;<=>?@[\]^_`{|}~—\"\-."
EXCESS_CHARS = f'[A-Za-z0-9{SPECIAL_CHARS}]+'
