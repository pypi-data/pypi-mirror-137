# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oarepo_model_builder_communities',
 'oarepo_model_builder_communities.invenio',
 'oarepo_model_builder_communities.models']

package_data = \
{'': ['*'], 'oarepo_model_builder_communities.invenio': ['templates/*']}

install_requires = \
['oarepo-model-builder>=0.9.24,<0.10.0']

entry_points = \
{'oarepo.models': ['oarepo-communities = '
                   'oarepo_model_builder_communities.models:communities.yaml'],
 'oarepo_model_builder.builders': ['0854-oarepo_communities_poetry = '
                                   'oarepo_model_builder_communities.invenio.poetry:OARepoCommunitiesPoetryBuilder'],
 'oarepo_model_builder.templates': ['101-communities_templates = '
                                    'oarepo_model_builder_communities.invenio']}

setup_kwargs = {
    'name': 'oarepo-model-builder-communities',
    'version': '1.0.0.dev3',
    'description': '',
    'long_description': '# oarepo-model-builder-communities',
    'author': 'Miroslav Bauer',
    'author_email': 'bauer@cesnet.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
