# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serverless',
 'serverless.aws',
 'serverless.aws.alerts',
 'serverless.aws.features',
 'serverless.aws.functions',
 'serverless.aws.iam',
 'serverless.integration',
 'serverless.service',
 'serverless.service.plugins']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'stringcase>=1.2.0,<2.0.0', 'troposphere>=3.2,<3.3']

setup_kwargs = {
    'name': 'serverless-builder',
    'version': '1.0.0',
    'description': 'Python interface to easily generate `serverless.yml`.',
    'long_description': '# serverless-builder\n\nPython interface to easily generate `serverless.yml`.\n\nMassive thanks goes to @dxd1 for his original idea and implementation.\n\n\n## Why\n\nserverless.yml easily can become a massive file with hundreds of lines even if you have only a couple of services.\nAdding plugins, features, naming patterns etc. become more and more complicated and each change can be really painful\ndue to multiple sections of the file which are affected.\n\n## How\n\nserverless-builder is an object oriented builder of the `serverless.yml` file with build in support for:\n\n- plugin management (with autoconfiguration)\n- function factory (with some best practice hints (DLQ))\n- autoconfiguration of some provider specific features like AWS X-Ray\n- monitoring support (wip)\n- easy resource manipulation with troposphere lib https://github.com/cloudtools/troposphere\n- easier IAM management with predefined permission sets\n- built-in support for any serverless attributes\n\n\n# Example\n\n```python\nfrom serverless.aws.functions.event_bridge import RetryPolicy\nfrom serverless.aws.functions.http import HTTPFunction\nfrom serverless import Service\nfrom serverless.provider import AWSProvider\nfrom serverless.aws.features import XRay\nfrom serverless.aws.iam.dynamodb import DynamoDBReader\nfrom serverless.plugins import ComposedVars, PythonRequirements, Prune\n\nfrom troposphere.dynamodb import Table, AttributeDefinition, KeySchema\n\nservice = Service(\n    "service-name",\n    "some dummy service",\n    AWSProvider()\n)\nservice.plugins.add(ComposedVars())\nservice.plugins.add(Prune())\nservice.plugins.add(PythonRequirements())\n\ntable = Table(\n    "TestTable",\n    BillingMode="PAY_PER_REQUEST",\n    AttributeDefinitions=[\n        AttributeDefinition(AttributeName="name", AttributeType="S")\n    ],\n    KeySchema=[KeySchema(AttributeName="name", KeyType="HASH")]\n)\n\nservice.enable(XRay())\nservice.provider.iam.apply(DynamoDBReader(table))\n\nservice.builder.function.generic("test", "description")\nservice.builder.function.http("test", "description", "/", HTTPFunction.POST)\n\n# Multiple events with different paths and/or methods can be set up for the same handler:\nservice.builder.function.http("test", "description", ["/", "/alias"], ["POST", "PUT"], handler="shared.handler")\n# This will add the same handler to all of these: POST /, POST /alias, PUT /, PUT /alias\n\nevent_bridge_function = service.builder.function.event_bridge(\n    "event_bridge_function",\n    "sample event bridge function",\n    "epsy",\n    {"source": ["saas.external"]},\n)\n\nevent_bridge_function.use_delivery_dlq(RetryPolicy(5, 300))\nevent_bridge_function.use_async_dlq()\n\nservice.resources.add(table)\n\nservice.render()\n```\n',
    'author': 'Epsy',
    'author_email': 'engineering@epsyhealth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/epsyhealth/serverless-builder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
