# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['robotoff',
 'robotoff.app',
 'robotoff.cli',
 'robotoff.elasticsearch',
 'robotoff.elasticsearch.category',
 'robotoff.elasticsearch.product',
 'robotoff.insights',
 'robotoff.prediction',
 'robotoff.prediction.category',
 'robotoff.prediction.category.neural',
 'robotoff.prediction.category.prediction_from_ocr',
 'robotoff.prediction.object_detection',
 'robotoff.prediction.object_detection.utils',
 'robotoff.prediction.ocr',
 'robotoff.scheduler',
 'robotoff.spellcheck',
 'robotoff.spellcheck.elasticsearch',
 'robotoff.spellcheck.patterns',
 'robotoff.spellcheck.percentages',
 'robotoff.spellcheck.vocabulary',
 'robotoff.utils',
 'robotoff.workers',
 'robotoff.workers.tasks']

package_data = \
{'': ['*'], 'robotoff.elasticsearch': ['index/*']}

install_requires = \
['APScheduler>=3.7.0,<3.8.0',
 'Pillow>=8.3.2,<8.4.0',
 'Pint==0.9',
 'dacite>=1.6.0,<1.7.0',
 'elasticsearch>=7.14.1,<7.15.0',
 'falcon-cors>=1.1.7,<1.2.0',
 'falcon-multipart>=0.2.0,<0.3.0',
 'falcon>=2.0.0,<2.1.0',
 'flashtext>=2.7,<2.8',
 'gunicorn>=20.1.0,<20.2.0',
 'influxdb>=5.3.1,<5.4.0',
 'jsonschema>=3.2.0,<3.3.0',
 'langid>=1.1.6,<1.2.0',
 'matplotlib>=3.4.3,<3.5.0',
 'more-itertools>=8.9.0,<8.10.0',
 'numpy>=1.19.5,<1.20.0',
 'orjson>=3.6.3,<3.7.0',
 'peewee>=3.14.4,<3.15.0',
 'protobuf>=3.17.3,<3.18.0',
 'psycopg2-binary>=2.9.1,<2.10.0',
 'py-healthcheck>=1.10.1,<2.0.0',
 'pymongo>=3.12.0,<3.13.0',
 'requests>=2.26.0,<2.27.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'scipy>=1.6.1,<1.7.0',
 'sentry-sdk[falcon]>=0.19.5,<0.20.0',
 'spacy>=2.3.7,<2.4.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['robotoff-cli = robotoff.cli.main:main']}

setup_kwargs = {
    'name': 'robotoff',
    'version': '1.1.0',
    'description': 'Real-time and batch prediction service for Openfoodfacts.',
    'long_description': None,
    'author': 'Openfoodfacts Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
