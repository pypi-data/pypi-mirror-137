#from x2cdict.google import GoogleVocabDict, GooglePhraseDict
from x2cdict.qishe import QisheVocabDict
from x2cdict.deeplearning import DeepLVocabDict, DeepLPhraseDict

class VocabDict:
  """
  It combines qishe and deepl voacb api
  """

  def __init__(self, from_lang, to_lang="cn"):
    self.from_lang, self.to_lang = from_lang, to_lang
    self.deepl_api = DeepLVocabDict(from_lang, to_lang)
    self.qishe_api = QisheVocabDict(from_lang, to_lang)

  def search(self, w, pos, google=True):
    result = self.qishe_api.search_with_pos(w, pos)
    if result == None:
      result = self.deepl_api.search(w, pos) if google else None
    return result

  def search_without_pos(self, w, google=True):
    result = self.qishe_api.search_without_pos(w)
    if result == None:
      result = self.deepl_api.search(w, None) if google else None
    return result


class PhraseDict:
  """
  DeepL API to translate phrase 
  """

  def __init__(self, from_lang, to_lang="cn"):
    self.from_lang, self.to_lang = from_lang, to_lang
    self.deepl_api = DeepLPhraseDict(from_lang, to_lang)

  def search(self, p):
    result = self.deepl_api.search(p)
    return result
