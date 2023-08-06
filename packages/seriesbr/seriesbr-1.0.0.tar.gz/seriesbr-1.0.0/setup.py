# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seriesbr', 'seriesbr.bcb', 'seriesbr.ibge', 'seriesbr.ipea', 'seriesbr.utils']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3.5,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'rope>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'seriesbr',
    'version': '1.0.0',
    'description': 'A Python library to interact with brazilian time series databases',
    'long_description': '# seriesbr: Uma biblioteca em Python para consultar bancos de dados com séries temporais do BCB, IPEA e IBGE\n\n[![pypi version](https://img.shields.io/pypi/v/seriesbr.svg)](https://pypi.org/project/seriesbr/)\n[![readthedocs status](https://readthedocs.org/projects/seriesbr/badge/?version=latest)](https://seriesbr.readthedocs.io/en/latest/?badge=latest)\n![codecov](https://codecov.io/gh/phelipetls/seriesbr/branch/master/graph/badge.svg)\n\n**seriesbr** ajuda a consultar, de forma programática, séries temporais dos\nbancos de dados do Banco Central do Brasil (BCB), Instituto de Pesquisa\nEconômica Aplicada (IPEA) e Instituto Brasileiro de Geografia e Estatística\n(IBGE).\n\nÉ inspirado nos seguintes pacotes escritos em R:\n[rbcb](https://github.com/wilsonfreitas/rbcb),\n[ipeaData](https://github.com/ipea/ipeaData) e\n[sidrar](https://github.com/cran/sidrar).\n\n# API\n\nA biblioteca possui três módulos, `bcb`, `ipea` e `ibge`. Cada uma possui uma\nfunção chamada `get_series` que aceita o identificador da série e retorna um\n[`DataFrame`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).\n\nPara mais detalhes, leia a [documentação](https://seriesbr.readthedocs.io/).\n\n# Exemplo\n\n```python\nfrom seriesbr import bcb\n\nbcb.get_series(20786, start="2015", end="2016")\n```\n\n```\n            20786\nDate\n2015-01-01  26.54\n2015-02-01  27.46\n2015-03-01  27.21\n2015-04-01  28.41\n2015-05-01  29.09\n2015-06-01  29.75\n2015-07-01  30.67\n2015-08-01  31.05\n2015-09-01  30.89\n2015-10-01  32.00\n2015-11-01  32.66\n2015-12-01  31.08\n2016-01-01  33.62\n2016-02-01  35.15\n2016-03-01  36.44\n2016-04-01  38.05\n2016-05-01  38.50\n2016-06-01  38.36\n2016-07-01  39.21\n2016-08-01  39.71\n2016-09-01  40.22\n2016-10-01  41.18\n2016-11-01  40.84\n2016-12-01  39.12\n```\n\n# Contribuindo\n\nSinta-se à vontade para abrir issues ou pull requests.\n\nCaso queira contribuir, primeiro instale o `poetry` e depois `poetry install`.\nRode os testes localmente com `poetry run pytest`.\n\n# Licença\n\n[MIT](https://github.com/phelipetls/seriesbr/blob/master/LICENSE)\n',
    'author': 'Phelipe Teles',
    'author_email': 'phelipe_teles@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phelipetls/seriesbr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
