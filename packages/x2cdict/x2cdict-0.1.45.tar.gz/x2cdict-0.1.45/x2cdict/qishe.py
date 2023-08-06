from x2cdict.db import ES2CN, EN2CN
from x2cdict.lib import gen_dictname
import os

class QisheVocabDict:

  APIS = {
    "es2cn": ES2CN,
    "en2cn": EN2CN
  }

  def __init__(self, from_lang, to_lang="cn"):
    self.from_lang, self.to_lang = from_lang, to_lang
    self.dictname = gen_dictname(self.from_lang, self.to_lang) 

    self.api = None
    if self.dictname in self.__class__.APIS.keys():
      self.api = self.__class__.APIS[self.dictname](os.getenv("DICT_DB_USER", "dict"), os.getenv("DICT_DB_PASS", "turingmachine"), os.getenv("DICT_DB_HOST", "127.0.0.1"))

  def search_with_pos(self, w, pos):
    if self.api == None:
      return None
    return self.api.search(w, pos)

  def search_without_pos(self, w):
    if self.api == None:
      return None
    return self.api.search_vocab(w)
