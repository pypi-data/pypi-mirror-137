from pymongo import MongoClient
from urllib.parse import quote_plus

class DB:
  """
  Encapsulation of mongodb
  """
  def __init__(self, dbname, user, password, host, authdb='admin'):
    uri = "mongodb://{}:{}@{}/{}".format(quote_plus(user), quote_plus(password), host, authdb)
    self.client = MongoClient(uri)
    self.db = self.client[dbname]
    self.vocabs = self.db.vocabs
    self.sentences = self.db.sentences

