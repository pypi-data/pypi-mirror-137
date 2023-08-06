# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linguadoc']

package_data = \
{'': ['*'], 'linguadoc': ['de/*', 'en/*', 'es/*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'python-docx>=0.8.11,<0.9.0']

entry_points = \
{'console_scripts': ['lingua_skdocx = linguadoc._entry:gen_lingua_docx']}

setup_kwargs = {
    'name': 'linguadoc',
    'version': '0.1.4',
    'description': 'DOC generator for language learning',
    'long_description': '# Installation\n\n```\npip3 install --verbose linguadoc \n```\n\n# Usage\n\nPlease refer to [api docs](https://qishe-nlp.github.io/linguadoc/).\n\n### Execute usage\n\n* Convert json into docx\n```\ngen_lingua_docx --sourcejson [source.json] --lang [en/de/es] --destdocx [output.docx] --title [test_title]\n```\n\n### Package usage\n```\n\n```\n\n# Development\n\n### Clone project\n```\ngit clone https://github.com/qishe-nlp/linguadoc.git\n```\n\n### Install [poetry](https://python-poetry.org/docs/)\n\n### Install dependencies\n```\npoetry update\n```\n\n### Test\n```\npoetry run pytest -rP --capture=sys\n```\nwhich run tests under `tests/*`\n\n\n### Execute\n```\npoetry run gen_lingua_docx --help\n```\n\n### Create sphinx docs\n```\npoetry shell\ncd apidocs\nsphinx-apidoc -f -o source ../linguadoc\nmake html\npython -m http.server -d build/html\n```\n\n### Host docs on github pages\n```\ncp -rf apidocs/build/html/* docs/\n```\n\n### Build\n* Change `version` in `pyproject.toml` and `linguadoc/__init__.py`\n* Build python package by `poetry build`\n\n### Git commit and push\n\n### Publish from local dev env\n* Set pypi test environment variables in poetry, refer to [poetry doc](https://python-poetry.org/docs/repositories/)\n* Publish to pypi test by `poetry publish -r test`\n\n### Publish through CI \n* Github action build and publish package to [test pypi repo](https://test.pypi.org/)\n\n```\ngit tag [x.x.x]\ngit push origin master\n```\n\n* Manually publish to [pypi repo](https://pypi.org/) through [github action](https://github.com/qishe-nlp/linguappt/actions/workflows/pypi.yml)\n\n',
    'author': 'Phoenix Grey',
    'author_email': 'phoenix.grey0108@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qishe-nlp/linguadoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
