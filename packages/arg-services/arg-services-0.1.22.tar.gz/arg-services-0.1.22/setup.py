# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arg_services',
 'arg_services.adu',
 'arg_services.adu.v1',
 'arg_services.base',
 'arg_services.base.v1',
 'arg_services.entailment',
 'arg_services.entailment.v1',
 'arg_services.graph',
 'arg_services.graph.v1',
 'arg_services.nlp',
 'arg_services.nlp.v1',
 'arg_services.retrieval',
 'arg_services.retrieval.v1',
 'arg_services.topic_modeling',
 'arg_services.topic_modeling.v1',
 'arg_services_helper']

package_data = \
{'': ['*']}

install_requires = \
['grpcio-reflection>=1.39.0,<2.0.0',
 'grpcio>=1.32,<2.0',
 'protobuf>=3.15.8,<4.0.0']

setup_kwargs = {
    'name': 'arg-services',
    'version': '0.1.22',
    'description': 'gRPC definitions for microservice-based argumentation machines',
    'long_description': '# Argumentation Microservices\n',
    'author': 'Mirko Lenz',
    'author_email': 'info@mirko-lenz.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://recap.uni-trier.de',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
