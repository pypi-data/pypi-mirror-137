# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_sqs_consumer']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.0,<2.0.0',
 'botocore>=1.20.0,<2.0.0',
 'single-source>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'aws-sqs-consumer',
    'version': '0.0.14',
    'description': 'AWS SQS Consumer',
    'long_description': '# Python AWS SQS Consumer\n\n[![PyPI](https://img.shields.io/pypi/v/aws-sqs-consumer?color=blue)](https://pypi.org/project/aws-sqs-consumer/)\n[![Build passing](https://github.com/HexmosTech/aws_sqs_consumer_python/actions/workflows/tests.yml/badge.svg?event=push)](https://github.com/HexmosTech/aws_sqs_consumer_python/actions/workflows/tests.yml)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/aws-sqs-consumer?color=g)\n\nWrite Amazon Simple Queue Service (SQS) consumers in Python with simplified interface. Define your logic to process an SQS message. After you\'re done processing, messages are deleted from the queue.\n\nCheckout the full documentation - [https://aws-sqs-consumer-python.readthedocs.io/en/latest/](https://aws-sqs-consumer-python.readthedocs.io/en/latest/)\n\n## Installation\n\n```\npip install aws-sqs-consumer\n```\n\n## Simple Usage\n\n```python\nfrom aws_sqs_consumer import Consumer, Message\n\nclass SimpleConsumer(Consumer):\n    def handle_message(self, message: Message):\n        # Write your logic to handle a single `message`.\n        print("Received message: ", message.Body)\n\nconsumer = SimpleConsumer(\n    queue_url="https://sqs.eu-west-1.amazonaws.com/12345678901/test_queue",\n    polling_wait_time_ms=5\n)\nconsumer.start()\n```\n\n## Contributing\n\nCheckout the Contribution guidelines - [CONTRIBUTING.md](CONTRIBUTING.md)\n',
    'author': 'Hexmos Technology',
    'author_email': 'nobody@flyweightgroup.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://aws-sqs-consumer-python.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
