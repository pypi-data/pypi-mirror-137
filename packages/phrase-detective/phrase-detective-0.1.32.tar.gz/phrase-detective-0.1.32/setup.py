# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phrase_detective',
 'phrase_detective.de',
 'phrase_detective.en',
 'phrase_detective.es',
 'phrase_detective.regx']

package_data = \
{'': ['*']}

install_requires = \
['spacy>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'phrase-detective',
    'version': '0.1.32',
    'description': 'Phrase recognizer component for spacy pipeline',
    'long_description': '# Installation from pip3\n\n```shell\npip3 install --verbose phrase_detective \npython -m spacy download en_core_web_trf\npython -m spacy download es_dep_news_trf\npython -m spacy download de_dep_news_trf\n```\n\n# Usage\n\nPlease refer to [api docs](https://qishe-nlp.github.io/phrase-detective/)\n\n### Detect noun phrases \n```\nimport spacy\nfrom spacy import Language\nfrom phrase_detective import NounPhraseRecognizer, PKG_INDICES\n\n@Language.factory("nprecog")\ndef create_np_parser(nlp: Language, name: str):\n  return NounPhraseRecognizer(nlp) \n\ndef noun_phrase(lang, sentence):\n  nlp = spacy.load(PKG_INDICES[lang])\n  nlp.add_pipe("nprecog")\n  doc = nlp(sentence)\n  for np in doc._.noun_phrases:\n    print(np.text)\n\n```\n### Detect verb phrases \n\n```\nimport spacy\nfrom spacy import Language\nfrom phrase_detective import VerbKnowledgeRecognizer, PKG_INDICES\n\n@Language.factory("vkbrecog")\ndef create_vkb_parser(nlp: Language, name: str):\n  return VerbKnowledgeRecognizer(nlp) \n\ndef verb_knowledge(lang, sentence):\n  nlp = spacy.load(PKG_INDICES[lang])\n  nlp.add_pipe("vkbrecog")\n  doc = nlp(sentence)\n  for v in doc._.verbs:\n    print("TEXT: {}, TAG: {}, FORM: {}, ORIGNAL: {}".format(v.text, v.tag_, spacy.explain(v.tag_), v.lemma_))\n  for pp in doc._.passive_phrases:\n    print(pp.text)\n  for vp in doc._.verb_phrases:\n    print(vp)\n```\n\n# Development\n\n### Clone project\n```\ngit clone https://github.com/qishe-nlp/phrase-detective.git\n```\n\n### Install [poetry](https://python-poetry.org/docs/)\n\n### Install dependencies\n```\npoetry update\n```\n\n### Test and Issue\n```\npoetry run pytest -rP\n```\nwhich run tests under `tests/*`\n\n### Create sphinx docs\n```\npoetry shell\ncd apidocs\nsphinx-apidoc -f -o source ../phrase_detective\nmake html\npython -m http.server -d build/html\n```\n\n### Hose docs on github pages\n```\ncp -rf apidocs/build/html/* docs/\n```\n\n### Build\n* Change `version` in `pyproject.toml` and `phrase_detective/__init__.py`\n* Build python package by `poetry build`\n\n### Git commit and push\n\n### Publish from local dev env\n* Set pypi test environment variables in poetry, refer to [poetry doc](https://python-poetry.org/docs/repositories/)\n* Publish to pypi test by `poetry publish -r test`\n\n### Publish through CI \n\n* Github action build and publish package to [test pypi repo](https://test.pypi.org/)\n\n```\ngit tag [x.x.x]\ngit push origin master\n```\n\n* Manually publish to [pypi repo](https://pypi.org/) through [github action](https://github.com/qishe-nlp/phrase-detective/actions/workflows/pypi.yml)\n\n',
    'author': 'Phoenix Grey',
    'author_email': 'phoenix.grey0108@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qishe-nlp/phrase-detective',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
