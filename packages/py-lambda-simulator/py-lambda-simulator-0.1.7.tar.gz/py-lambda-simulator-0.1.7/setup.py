# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_lambda_simulator']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'asyncer>=0.0.1,<0.0.2',
 'boto3>=1.20.46,<2.0.0',
 'moto>=3.0.2,<4.0.0',
 'typing-extensions>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'py-lambda-simulator',
    'version': '0.1.7',
    'description': '',
    'long_description': '# py-lambda-simulator\n\npy-lambda-simulator is a Python library for running aws-lambda functions locally.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install py-lambda-simulator.\n\n```bash\npip install py-lambda-simulator\n```\n\n## Usage\n\n```python\nimport asyncio\nimport json\nfrom asyncio import run\n\nfrom py_lambda_simulator.lambda_simulator import AwsSimulator\nfrom py_lambda_simulator.sqs_lambda_simulator import SqsLambdaSimulator, SqsEvent, LambdaSqsFunc\n\n\nasync def example(simulator, aws_simulator):\n    queue = aws_simulator.create_sqs_queue("queue-name")\n\n    def sqs_handler(event: SqsEvent, context):\n        print(event["Records"][0]["body"])\n\n    simulator.add_func(LambdaSqsFunc(name="test-sqs-lambda", queue_name="queue-name", handler_func=sqs_handler))\n\n    async def send_msg():\n        while True:\n            aws_simulator.get_sqs_client().send_message(\n                QueueUrl=queue["queue_url"], MessageBody=json.dumps({"test": 123})\n            )\n            await asyncio.sleep(1)\n\n    await asyncio.gather(simulator.start(), send_msg())\n\n\nif __name__ == \'__main__\':\n    _simulator = SqsLambdaSimulator()\n    _aws_simulator = AwsSimulator()\n    run(example(_simulator, _aws_simulator))\n```\n\nFor more examples see the tests.\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'Johan Bothin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hemma/py-lambda-simulator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
