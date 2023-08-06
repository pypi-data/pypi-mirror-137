# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oarepo_model_builder_multilingual',
 'oarepo_model_builder_multilingual.invenio',
 'oarepo_model_builder_multilingual.model_preprocessors',
 'oarepo_model_builder_multilingual.property_preprocessors',
 'oarepo_model_builder_multilingual.schema']

package_data = \
{'': ['*'], 'oarepo_model_builder_multilingual.invenio': ['templates/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'click>=7.1',
 'isort>=5.10.1,<6.0.0',
 'jsonpointer>=2.2,<3.0',
 'langcodes>=3.3.0',
 'libcst>=0.4.1,<0.5.0',
 'marshmallow>=3.14.1,<4.0.0',
 'oarepo-model-builder>=0.9.17',
 'tomlkit>=0.9.0,<0.10.0']

extras_require = \
{'json5': ['json5>=0.9.6,<0.10.0'], 'pyyaml': ['PyYAML>=6.0,<7.0']}

entry_points = \
{'oarepo.model_schemas': ['es-strings = '
                          'oarepo_model_builder_multilingual:multilingual_jsonschema.json5',
                          'mult-settings = '
                          'oarepo_model_builder_multilingual:multilingual_settings.json5'],
 'oarepo_model_builder.builders': ['0901-invenio_multiligual_poetry = '
                                   'oarepo_model_builder_multilingual.invenio.invenio_multilingual_poetry:InvenioMultilingualPoetryBuilder',
                                   '360-invenio_record_multilingual_dumper = '
                                   'oarepo_model_builder_multilingual.invenio.invenio_record_dumper_multilingual:InvenioRecordMultilingualDumperBuilder'],
 'oarepo_model_builder.model_preprocessors': ['30-multilingual = '
                                              'oarepo_model_builder_multilingual.model_preprocessors.multilingual:MultilingualModelPreprocessor'],
 'oarepo_model_builder.property_preprocessors': ['700-multilingual = '
                                                 'oarepo_model_builder_multilingual.property_preprocessors.multilingual:MultilangPreprocessor'],
 'oarepo_model_builder.templates': ['100-multilingual_templates = '
                                    'oarepo_model_builder_multilingual.invenio']}

setup_kwargs = {
    'name': 'oarepo-model-builder-multilingual',
    'version': '0.1.0',
    'description': '',
    'long_description': '# OARepo model builder multilingual\n\n',
    'author': 'Alzbeta Pokorna',
    'author_email': 'alzbeta.pokorna@cesnet.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
