# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['x2cdict', 'x2cdict.db']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'deepl>=1.3.1,<2.0.0',
 'googletrans==4.0.0-rc1',
 'pymongo>=3.10.1,<4.0.0']

entry_points = \
{'console_scripts': ['x2cdict_phrase = x2cdict.entry:search_phrase',
                     'x2cdict_vocab = x2cdict.entry:search_vocab',
                     'x2cdict_vocab_without_pos = '
                     'x2cdict.entry:search_vocab_without_pos']}

setup_kwargs = {
    'name': 'x2cdict',
    'version': '0.1.45',
    'description': 'translate X language into Chinese',
    'long_description': '# Installation\n\n```\npip3 install --verbose x2cdict \n```\n\n# Usage\n### Environment setting\n\n* `DICT_DB_HOST` is `127.0.0.1` by default\n* `DICT_DB_USER` is `dict` by default\n* `DICT_DB_PASS` is `turingmachine` by default\n\n\nThe dictionary db IS NOT BUILT in this project, you HAVE TO install the DB by yourself, refer to [BaJiu Dictionary Installation](https://github.com/bajiu-dict/deploy_dict_mongo).\n\n### Binary Usage\n\n* Search vocabs with PoS assgined\n```\nx2cdict_vocab --fromlang en --tolang cn --pos ADJ --word happy --google False\nx2cdict_vocab --help\n```\n\n* Search vocabs without PoS\n```\nx2cdict_vocab_without_pos --fromlang en --tolang cn --word happy --google False\nx2cdict_vocab_without_pos --help\n```\n\n* Search phrase\n```\nx2cdict_phrase --fromlang en --tolang cn --phrase "overcome the problem"\nx2cdict_phrase --help\n```\n\n### Issues\n\n* PATH issue:\n  * The folder where the exectuable is installed may not be in your `PATH`. For Linux, check the `$HOME/.local/bin` to see whether the executable `x2cdict_*` is installed.\n  * Add `export PATH="$HOME/.local/bin:$PATH"` in `$HOME/.bashrc`\n\n* hpack issue:\n  ```\n  pip3 uninstall hpack\n  pip3 install hpack==3.0.0\n  ```\n\n### Package Usage\n```\nfrom x2cdict import VocabDict, PhraseDict\ndef search_vocab(word, pos, fromlang, tolang, google):\n  vd = VocabDict(fromlang, tolang)\n  r = vd.search(word, pos, google)\n  print(r)\n\ndef search_vocab_without_pos(word, fromlang, tolang, google):\n  vd = VocabDict(fromlang, tolang)\n  r = vd.search_without_pos(word, google)\n  print(r)\n\ndef search_phrase(phrase, fromlang, tolang):\n  vd = PhraseDict(fromlang, tolang)\n  r = vd.search(phrase)\n  print(r)\n```\n\nFrom above, `google` is a boolean variable to switch whether using google translation, default is `True`.\n\n# Development\n\n### Clone the project\n```\ngit clone https://github.com/qishe-nlp/x2cdict.git\n```\n\n### Install [poetry](https://python-poetry.org/docs/)\n\n### Install dependencies\n```\npoetry update\n```\n\n### Test\n```\npoetry run pytest -rP\n```\nwhich run tests under `tests/*`\n\n### Execute\n```\npoetry run x2cdict_vocab --help\npoetry run x2cdict_vocab_without_pos --help\npoetry run xc2dict_phrase --help\n```\n\n### Build\n* Change `version` in\n  * `pyproject.toml`\n  * `x2cdict/__init__.py`\n  * `tests/test_x2cdict.py`\n* Build python package by `poetry build`\n\n### Publish from local dev env\n* Set pypi test environment variables in poetry, refer to [poetry doc](https://python-poetry.org/docs/repositories/)\n* Publish to pypi test by `poetry publish -r test`\n\n### Publish through CI \n\n* Github action build and publish package to [test pypi repo](https://test.pypi.org/)\n\n```\ngit tag [x.x.x]\ngit push origin master\n```\n\n* Manually publish to [pypi repo](https://pypi.org/) through [github action](https://github.com/qishe-nlp/x2cdict/actions/workflows/pypi.yml)\n',
    'author': 'Phoenix Grey',
    'author_email': 'phoenix.grey0108@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qishe-nlp/x2cdict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
