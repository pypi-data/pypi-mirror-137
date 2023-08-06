from x2cdict.db.db import DB
from x2cdict.posmap import POSMAP

class ES2CN(DB):
  """
  Encapsulation of mongodb
  """
  def __init__(self, user, password, host, authdb='admin'):
    self.dictname = 'es2cn'
    self.posmap = POSMAP['es']
    super().__init__(self.dictname, user, password, host, authdb)
    self.verbs_extension = self.db.verbs_extension
    self.verbs_inverse_variation = self.db.verbs_inverse_variation

  def search_sentences(self, vocab):
    result = list(self.sentences.find({"original": {"$regex": ".* "+vocab+" .*"}}, {"_id": 0}))[:2]
    return result

  def search_vocab(self, text):
    result = self.vocabs.find_one({"word": text})
    if result != None:
      del result['_id']
    return result 

  def search_verb_extension(self, text):
    result = self.verbs_extension.find_one({"word": text})
    return result 

  def search_verb_inverse_variation(self, text):
    result = self.verbs_inverse_variation.find_one({"word": text})
    return result 

  def verb_original(self, w, _pos):
    result = None
    verb = self.search_vocab(w)
    if verb != None:
      ex = verb["explanation"]

      e = None
      for i in ex:
        if i["pos"] in _pos:
          e = i
          break
 
      if e != None:
        result = {
          "word": w,
          "explanation": e,
          "variations": {
            "origin": w
          },
          "from": self.dictname 
        }

        vv = self.search_verb_extension(w) 
        if vv != None:
          result["extension"] = vv["extension"] 

      return result

  def verb_variation(self, w, _pos):
    result = None
    verb = self.search_verb_inverse_variation(w)
    if verb != None:
      original_verb = verb["variations"]["original"]
      info = self.verb_original(original_verb, _pos)
      if info != None:
        result = {
          "word": w,
          "explanation": info["explanation"],
          "variations": verb["variations"],
          "from": self.dictname
        }
        if "extension" in info.keys():
          result["extension"] = info["extension"]
    return result

  def other_vocab(self, w, _pos):
    result = None
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
          "explanation": e,
          "from": self.dictname 
        }
    return result

  def _search(self, w, pos):
    result = None

    _pos = self.posmap[pos] if pos in self.posmap.keys() else [pos] 

    if pos == "VERB" or pos == "AUX":
      result = self.verb_original(w, _pos)
      if result == None:
        result = self.verb_variation(w, _pos)
    else:
      result = self.other_vocab(w, _pos)
    return result

  def search(self, w, pos):
    result = self._search(w, pos)
    e = None
    if result != None:
      e = {}
      e['word'] = result['word']
      e['meaning'] = result['explanation']['meaning']
      e['dict_pos'] = result['explanation']['pos']
      e['from'] = result['from']
      if e['dict_pos'] not in self.posmap['VERB']:
        e['extension'] = result['explanation']['extension'] if 'extension' in result['explanation'].keys() else None
        e['variations'] = None
      else:
        e['extension'] = result['extension'] if 'extension' in result.keys() else None
        e['variations'] = result['variations'] if 'variations' in result.keys() else None
      e['examples'] = self.search_sentences(w)
    return e
