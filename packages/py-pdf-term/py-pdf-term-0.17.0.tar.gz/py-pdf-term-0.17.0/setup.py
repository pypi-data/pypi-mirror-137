# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_pdf_term',
 'py_pdf_term._common',
 'py_pdf_term.analysis',
 'py_pdf_term.analysis._analysis',
 'py_pdf_term.analysis._analysis.concats',
 'py_pdf_term.analysis._analysis.cooccurrences',
 'py_pdf_term.analysis._analysis.occurrences',
 'py_pdf_term.candidates',
 'py_pdf_term.candidates._candidates',
 'py_pdf_term.candidates._candidates.augmenters',
 'py_pdf_term.candidates._candidates.filters',
 'py_pdf_term.candidates._candidates.filters.term',
 'py_pdf_term.candidates._candidates.filters.term.concatenation',
 'py_pdf_term.candidates._candidates.filters.term.numeric',
 'py_pdf_term.candidates._candidates.filters.term.propernoun',
 'py_pdf_term.candidates._candidates.filters.term.symbollike',
 'py_pdf_term.candidates._candidates.filters.token',
 'py_pdf_term.candidates._candidates.splitters',
 'py_pdf_term.endtoend',
 'py_pdf_term.endtoend._endtoend',
 'py_pdf_term.endtoend._endtoend.caches',
 'py_pdf_term.endtoend._endtoend.caches.candidate',
 'py_pdf_term.endtoend._endtoend.caches.method',
 'py_pdf_term.endtoend._endtoend.caches.styling',
 'py_pdf_term.endtoend._endtoend.caches.xml',
 'py_pdf_term.endtoend._endtoend.configs',
 'py_pdf_term.endtoend._endtoend.layers',
 'py_pdf_term.endtoend._endtoend.mappers',
 'py_pdf_term.endtoend._endtoend.mappers.caches',
 'py_pdf_term.endtoend._endtoend.mappers.candidates',
 'py_pdf_term.endtoend._endtoend.mappers.methods',
 'py_pdf_term.endtoend._endtoend.mappers.pdftoxml',
 'py_pdf_term.endtoend._endtoend.mappers.stylings',
 'py_pdf_term.methods',
 'py_pdf_term.methods._methods',
 'py_pdf_term.methods._methods.collectors',
 'py_pdf_term.methods._methods.rankers',
 'py_pdf_term.methods._methods.rankingdata',
 'py_pdf_term.pdftoxml',
 'py_pdf_term.pdftoxml._pdftoxml',
 'py_pdf_term.stylings',
 'py_pdf_term.stylings._stylings',
 'py_pdf_term.stylings._stylings.scores',
 'py_pdf_term.techterms',
 'py_pdf_term.techterms._techterms',
 'py_pdf_term.tokenizer',
 'py_pdf_term.tokenizer._tokenizer',
 'py_pdf_term.tokenizer._tokenizer.langs']

package_data = \
{'': ['*']}

install_requires = \
['pdfminer.six>=20211012,<20211013', 'spacy>=3.2.1,<4.0.0']

setup_kwargs = {
    'name': 'py-pdf-term',
    'version': '0.17.0',
    'description': 'A fully-configurable terminology extraction module written in Python',
    'long_description': '# py-pdf-term\n\nA fully-configurable terminology extraction module written in Python\n\n## Installation\n\n```\npip install py-pdf-term\n```\n\nYou also need to install spaCy models `ja_core_news_sm` and `en_core_web_sm`, which this module depends on.\n\n```\npip install https://github.com/explosion/spacy-models/releases/download/ja_core_news_sm-3.2.0/ja_core_news_sm-3.2.0.tar.gz\npip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.2.0/en_core_web_sm-3.2.0.tar.gz\n```\n\n## Documentation\n\nhttps://kumachan-mis.github.io/py-pdf-term\n',
    'author': 'Yuya Suwa',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kumachan-mis/py-pdf-term',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
