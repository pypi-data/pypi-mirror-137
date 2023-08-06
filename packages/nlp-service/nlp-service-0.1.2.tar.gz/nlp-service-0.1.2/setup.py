# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlp_service']

package_data = \
{'': ['*']}

install_requires = \
['arg-services>=0.1.22,<0.2.0',
 'grpcio>=1.43.0,<2.0.0',
 'numpy>=1.22.2,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'spacy>=3.2.1,<4.0.0']

extras_require = \
{'server': ['tensorflow>=2.8.0,<3.0.0',
            'sentence-transformers>=2.1.0,<3.0.0',
            'tensorflow-hub>=0.12.0,<0.13.0',
            'gensim>=4.1.2,<5.0.0',
            'pyemd>=0.5.1,<0.6.0',
            'typer>=0.4.0,<0.5.0',
            'python-Levenshtein>=0.12.2,<0.13.0',
            'torch>=1.10.2,<2.0.0'],
 'wmd': ['gensim>=4.1.2,<5.0.0']}

setup_kwargs = {
    'name': 'nlp-service',
    'version': '0.1.2',
    'description': 'Microservice for NLP tasks using gRPC',
    'long_description': '# NLP Microservice\n',
    'author': 'Mirko Lenz',
    'author_email': 'info@mirko-lenz.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://recap.uni-trier.de',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
