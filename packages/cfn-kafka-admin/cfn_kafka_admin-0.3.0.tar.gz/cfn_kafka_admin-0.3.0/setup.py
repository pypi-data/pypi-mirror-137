# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfn_kafka_admin',
 'cfn_kafka_admin.cfn_resources_definitions',
 'cfn_kafka_admin.kafka',
 'cfn_kafka_admin.lambda_functions',
 'cfn_kafka_admin.models',
 'cfn_kafka_admin.specs']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aws-cfn-custom-resource-resolve-parser>=0.2.1,<0.3.0',
 'cfn-resource-provider>=1.0.7,<2.0.0',
 'compose-x-common[aws]>=0.2.3,<0.3.0',
 'datamodel-code-generator[http]>=0.11.17,<0.12.0',
 'importlib-resources>=5.4.0,<6.0.0',
 'jsonschema>=4.4.0,<5.0.0',
 'kafka-python>=2.0.2,<3.0.0',
 'kafka-schema-registry-admin>=0.1.0,<0.2.0',
 'troposphere>=3.2.2,<4.0.0']

entry_points = \
{'console_scripts': ['aws-cfn-kafka-admin-provider = cfn_kafka_admin.cli:main']}

setup_kwargs = {
    'name': 'cfn-kafka-admin',
    'version': '0.3.0',
    'description': 'AWS CloudFormation Resources to manage Kafka',
    'long_description': '===============\ncfn-kafka-admin\n===============\n\n------------------------------------------------------------------------------\nCLI Tool and Lambda Functions to CRUD Kafka resources via AWS CloudFormation\n------------------------------------------------------------------------------\n\n\n|PYPI_VERSION|\n\n|FOSSA| |PYPI_LICENSE|\n\n|CODE_STYLE| |TDD|\n\n.. image:: https://codebuild.eu-west-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiY2xwc0NER1JuU1J3MThYczhFMDJLWlQxWGpoRnhNWHNtbGN1NGpVMVNTMk12UlQxdWVlZ2w5YnhPQzhkMnV4cTI0S0tIdTRyTmRHWWErWXJPNWFpcWlzPSIsIml2UGFyYW1ldGVyU3BlYyI6IkxaRGZCMW1KbVE1RWRJYjciLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main\n        :target: https://eu-west-1.codebuild.aws.amazon.com/project/eyJlbmNyeXB0ZWREYXRhIjoibVAvWVBBNjZlNWFwTWEwSEdWcGx6MWpudy9KeEZTb1lXdWFuQ3FwbjJCRTBnc1lyZm41eHRqV2k0bDN6UTBmaEpJMGd0Y3I3Vm5kTGtZQzc1b25Uckxxd3hERzlpSzJndVFOekJUR0NMM0V0YXljSWx4Yjc2YmJpUzlZM01RPT0iLCJpdlBhcmFtZXRlclNwZWMiOiI3bnllb1dlbU8rZis1ekh5IiwibWF0ZXJpYWxTZXRTZXJpYWwiOjF9\n\n\nManage Kafka resources via AWS CFN\n===================================\n\n* Topics\n* ACLs\n* Schemas (non AWS Glue Schema)\n\n\n* Free software: MPL-2.0\n* Documentation: https://cfn-kafka-admin.readthedocs.io.\n\n.. |PYPI_VERSION| image:: https://img.shields.io/pypi/v/cfn-kafka-admin.svg\n        :target: https://pypi.python.org/pypi/cfn-kafka-admin\n\n.. |PYPI_LICENSE| image:: https://img.shields.io/pypi/l/cfn-kafka-admin\n    :alt: PyPI - License\n    :target: https://github.com/compose-x/cfn-kafka-admin/blob/master/LICENSE\n\n.. |PYPI_PYVERS| image:: https://img.shields.io/pypi/pyversions/cfn-kafka-admin\n    :alt: PyPI - Python Version\n    :target: https://pypi.python.org/pypi/cfn-kafka-admin\n\n.. |PYPI_WHEEL| image:: https://img.shields.io/pypi/wheel/cfn-kafka-admin\n    :alt: PyPI - Wheel\n    :target: https://pypi.python.org/pypi/cfn-kafka-admin\n\n.. |FOSSA| image:: https://app.fossa.com/api/projects/git%2Bgithub.com%2Fcompose-x%2Fcfn-kafka-admin.svg?type=shield\n\n.. |CODE_STYLE| image:: https://img.shields.io/badge/codestyle-black-black\n    :alt: CodeStyle\n    :target: https://pypi.org/project/black/\n\n.. |TDD| image:: https://img.shields.io/badge/tdd-pytest-black\n    :alt: TDD with pytest\n    :target: https://docs.pytest.org/en/latest/contents.html\n\n.. |BDD| image:: https://img.shields.io/badge/bdd-behave-black\n    :alt: BDD with Behave\n    :target: https://behave.readthedocs.io/en/latest/\n',
    'author': 'johnpreston',
    'author_email': 'john@compose-x.io',
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
