from x2cdict import VocabDict, PhraseDict
import click

@click.command()
@click.option("--word", help="Specify the word to look up", prompt="word")
@click.option("--pos", help="Specify PoS of the word", default=None)
@click.option("--fromlang", help="Specify the language of the word", prompt="translate from")
@click.option("--tolang", help="Specify the language the word to be translated into", prompt="translate to", default="cn")
@click.option("--google", help="Whether using google for secondary source", prompt="using google", type=bool, default=True)
def search_vocab(word, pos, fromlang, tolang, google):
  vd = VocabDict(fromlang, tolang)
  r = vd.search(word, pos, google)
  print(r)


@click.command()
@click.option("--word", help="Specify the word to look up", prompt="word")
@click.option("--fromlang", help="Specify the language of the word", prompt="translate from")
@click.option("--tolang", help="Specify the language the word to be translated into", prompt="translate to", default="cn")
@click.option("--google", help="Whether using google for secondary source", prompt="using google", type=bool, default=True)
def search_vocab_without_pos(word, fromlang, tolang, google):
  vd = VocabDict(fromlang, tolang)
  r = vd.search_without_pos(word, google)
  print(r)


@click.command()
@click.option("--phrase", help="Specify the phrase to look up", prompt="phrase")
@click.option("--fromlang", help="Specify the language of the word", prompt="translate from")
@click.option("--tolang", help="Specify the language the word to be translated into", prompt="translate to", default="cn")
def search_phrase(phrase, fromlang, tolang):
  vd = PhraseDict(fromlang, tolang)
  r = vd.search(phrase)
  print(r)

