# Installation

```
pip3 install --verbose x2cdict 
```

# Usage
### Environment setting

* `DICT_DB_HOST` is `127.0.0.1` by default
* `DICT_DB_USER` is `dict` by default
* `DICT_DB_PASS` is `turingmachine` by default


The dictionary db IS NOT BUILT in this project, you HAVE TO install the DB by yourself, refer to [BaJiu Dictionary Installation](https://github.com/bajiu-dict/deploy_dict_mongo).

### Binary Usage

* Search vocabs with PoS assgined
```
x2cdict_vocab --fromlang en --tolang cn --pos ADJ --word happy --google False
x2cdict_vocab --help
```

* Search vocabs without PoS
```
x2cdict_vocab_without_pos --fromlang en --tolang cn --word happy --google False
x2cdict_vocab_without_pos --help
```

* Search phrase
```
x2cdict_phrase --fromlang en --tolang cn --phrase "overcome the problem"
x2cdict_phrase --help
```

### Issues

* PATH issue:
  * The folder where the exectuable is installed may not be in your `PATH`. For Linux, check the `$HOME/.local/bin` to see whether the executable `x2cdict_*` is installed.
  * Add `export PATH="$HOME/.local/bin:$PATH"` in `$HOME/.bashrc`

* hpack issue:
  ```
  pip3 uninstall hpack
  pip3 install hpack==3.0.0
  ```

### Package Usage
```
from x2cdict import VocabDict, PhraseDict
def search_vocab(word, pos, fromlang, tolang, google):
  vd = VocabDict(fromlang, tolang)
  r = vd.search(word, pos, google)
  print(r)

def search_vocab_without_pos(word, fromlang, tolang, google):
  vd = VocabDict(fromlang, tolang)
  r = vd.search_without_pos(word, google)
  print(r)

def search_phrase(phrase, fromlang, tolang):
  vd = PhraseDict(fromlang, tolang)
  r = vd.search(phrase)
  print(r)
```

From above, `google` is a boolean variable to switch whether using google translation, default is `True`.

# Development

### Clone the project
```
git clone https://github.com/qishe-nlp/x2cdict.git
```

### Install [poetry](https://python-poetry.org/docs/)

### Install dependencies
```
poetry update
```

### Test
```
poetry run pytest -rP
```
which run tests under `tests/*`

### Execute
```
poetry run x2cdict_vocab --help
poetry run x2cdict_vocab_without_pos --help
poetry run xc2dict_phrase --help
```

### Build
* Change `version` in
  * `pyproject.toml`
  * `x2cdict/__init__.py`
  * `tests/test_x2cdict.py`
* Build python package by `poetry build`

### Publish from local dev env
* Set pypi test environment variables in poetry, refer to [poetry doc](https://python-poetry.org/docs/repositories/)
* Publish to pypi test by `poetry publish -r test`

### Publish through CI 

* Github action build and publish package to [test pypi repo](https://test.pypi.org/)

```
git tag [x.x.x]
git push origin master
```

* Manually publish to [pypi repo](https://pypi.org/) through [github action](https://github.com/qishe-nlp/x2cdict/actions/workflows/pypi.yml)
