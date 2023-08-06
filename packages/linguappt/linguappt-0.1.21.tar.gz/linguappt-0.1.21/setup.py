# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linguappt',
 'linguappt._entry',
 'linguappt.de',
 'linguappt.en',
 'linguappt.es']

package_data = \
{'': ['*'],
 'linguappt.de': ['templates/*'],
 'linguappt.en': ['templates/*'],
 'linguappt.es': ['templates/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'pdf2image>=1.12.1,<2.0.0',
 'python-pptx>=0.6.18,<0.7.0']

entry_points = \
{'console_scripts': ['lingua_meta2media = linguappt._entry.command:meta2media',
                     'lingua_phraseppt = linguappt._entry.command:phraseppt',
                     'lingua_pptx2pdf2images = '
                     'linguappt._entry.command:pptx2pdf2images',
                     'lingua_pptx_validate = '
                     'linguappt._entry.validation:validate',
                     'lingua_structurekgppt = '
                     'linguappt._entry.command:structurekgppt',
                     'lingua_vocabppt = linguappt._entry.command:vocabppt']}

setup_kwargs = {
    'name': 'linguappt',
    'version': '0.1.21',
    'description': 'PPT generator for language learning',
    'long_description': '# Installation\n\n```\npip3 install --verbose linguappt \n```\n\n# Usage\n\nPlease refer to [api docs](https://qishe-nlp.github.io/linguappt/).\n\n### Execute usage\n\n* Validate ppt template\n```\nlingua_pptx_validate --pptx [pptx file]\n```\n\n* Convert vocabulary csv file into ppt file\n```\nlingua_vocabppt --sourcecsv [vocab csv file] --lang [language] --title [title shown in ppt] --destpptx [pptx file]\n```\n\n* Convert phrase csv file into ppt file\n```\nlingua_phraseppt --sourcecsv [phrase csv file] --lang [language] --title [title shown in ppt] --destpptx [pptx file]\n```\n\n\n* Convert ppt into pdf\n```\nlingua_pptx2pdf --sourcepptx [pptx file] --destdir [dest directory storing pdf and images]\n```\n\n### Package usage\n```\nfrom linguappt import SpanishVocabPPT, EnglishVocabPPT\nfrom linguappt import EnglishPhrasePPT, SpanishPhrasePPT\n\ndef vocabppt(sourcecsv, title, lang, destpptx):\n  _PPTS = {\n    "en": EnglishVocabPPT,\n    "es": SpanishVocabPPT\n  }\n\n  _PPT = _PPTS[lang]\n\n  vp = _PPT(sourcecsv, title)\n  vp.convert_to_ppt(destpptx)\n\ndef phraseppt(sourcecsv, title, lang, destpptx):\n  _PPTS = {\n    "en": EnglishPhrasePPT,\n    "es": SpanishPhrasePPT\n  }\n\n  _PPT = _PPTS[lang]\n\n  vp = _PPT(sourcecsv, title)\n  vp.convert_to_ppt(destpptx)\n\n\n```\n\n# Development\n\n### Clone project\n```\ngit clone https://github.com/qishe-nlp/linguappt.git\n```\n\n### Install [poetry](https://python-poetry.org/docs/)\n\n### Install dependencies\n```\npoetry update\n```\n\n### Test\n```\npoetry run pytest -rP --capture=sys\n```\nwhich run tests under `tests/*`\n\n\n### Execute\n```\npoetry run lingua_pptx_validate --help\npoetry run lingua_vocabppt --help\npoetry run lingua_phraseppt --help\n\npoetry run lingua_pptx2pdf2images --help\npoetry run lingua_csv2media --help\n```\n\n### Create sphinx docs\n```\npoetry shell\ncd apidocs\nsphinx-apidoc -f -o source ../linguappt\nmake html\npython -m http.server -d build/html\n```\n\n### Host docs on github pages\n```\ncp -rf apidocs/build/html/* docs/\n```\n\n### Build\n* Change `version` in `pyproject.toml` and `linguappt/__init__.py`\n* Build python package by `poetry build`\n\n### Git commit and push\n\n### Publish from local dev env\n* Set pypi test environment variables in poetry, refer to [poetry doc](https://python-poetry.org/docs/repositories/)\n* Publish to pypi test by `poetry publish -r test`\n\n### Publish through CI \n* Github action build and publish package to [test pypi repo](https://test.pypi.org/)\n\n```\ngit tag [x.x.x]\ngit push origin master\n```\n\n* Manually publish to [pypi repo](https://pypi.org/) through [github action](https://github.com/qishe-nlp/linguappt/actions/workflows/pypi.yml)\n\n',
    'author': 'Phoenix Grey',
    'author_email': 'phoenix.grey0108@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qishe-nlp/linguappt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
