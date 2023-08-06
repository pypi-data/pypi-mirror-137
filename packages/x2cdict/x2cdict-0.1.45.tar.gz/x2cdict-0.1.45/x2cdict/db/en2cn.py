from x2cdict.db.db import DB
from x2cdict.posmap import POSMAP


class EN2CN(DB):
  """
  Encapsulation of mongodb
  """
  def __init__(self, user, password, host, authdb='admin'):
    self.dictname = 'en2cn'
    self.posmap = POSMAP['en']
    super().__init__(self.dictname, user, password, host, authdb)

  def search_vocab(self, text):
    result = self.vocabs.find_one({"word": text})
    if result != None:
      del result["_id"]
    return result 

  def search_sentences(self, vocab):
    result = list(self.sentences.find({"original": {"$regex": ".* "+vocab+" .*"}}, {"_id": 0}))[:2]
    return result

  def search(self, w, pos):
    result = None

    _pos = self.posmap[pos] if pos in self.posmap.keys() else [pos] 

    _r = self.search_vocab(w)
    if _r != None:
      ex = _r["explanation"]

      e = None # default: None 
      for i in ex:
        if i["pos"] in _pos:
          e = i
          break
 
      if e != None: 
        result = {
          "word": w,
          "dict_pos": e['pos'],
          "meaning": e['meaning'],
          "from": self.dictname 
        }
        result['variations'] = e['variations'] if 'variations' in e.keys() else None
        result['extension'] = e['extension'] if 'extension' in e.keys() else None
        result['examples'] = self.search_sentences(w)
    return result
