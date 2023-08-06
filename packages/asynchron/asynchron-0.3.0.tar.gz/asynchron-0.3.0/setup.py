# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['asynchron',
 'asynchron.amqp',
 'asynchron.amqp.consumer',
 'asynchron.amqp.publisher',
 'asynchron.amqp.serializer',
 'asynchron.codegen',
 'asynchron.codegen.generator',
 'asynchron.codegen.generator.jinja',
 'asynchron.codegen.spec',
 'asynchron.codegen.spec.reader',
 'asynchron.codegen.spec.transformer',
 'asynchron.codegen.spec.viewer',
 'asynchron.codegen.spec.visitor',
 'asynchron.codegen.spec.walker',
 'asynchron.codegen.writer',
 'asynchron.core']

package_data = \
{'': ['*'],
 'asynchron.codegen.generator.jinja': ['templates/*', 'templates/base/*']}

extras_require = \
{'aio-pika': ['pydantic>=1.8.2,<2.0.0', 'aio-pika>=6.8.0,<7.0.0'],
 'codegen': ['Jinja2>=3.0.3,<4.0.0',
             'pydantic>=1.8.2,<2.0.0',
             'PyYAML>=6.0,<7.0',
             'click>=8.0.3,<9.0.0',
             'dependency-injector>=4.37.0,<5.0.0',
             'jsonschema>=4.2.1,<5.0.0',
             'stringcase>=1.2.0,<2.0.0']}

entry_points = \
{'console_scripts': ['asynchron-codegen = asynchron.codegen.cli:cli']}

setup_kwargs = {
    'name': 'asynchron',
    'version': '0.3.0',
    'description': 'Python service framework with code generator based on AsyncAPI specification',
    'long_description': '# asynchron\n\nPython service framework with code generator based on AsyncAPI specification\n\n## Usage example\n\n1) install and run codegen\n    ```bash\n    poetry add asynchron -E codegen\n    poetry run asynchron-codegen -f /path/to/asyncapi.yaml generate python-aio-pika -o /output/dir\n    ```\n2) install dependencies for you generated code\n    ```bash\n    poetry add asynchron -E aio-pika\n    ```\n\n## Development\n\nUse bash script to install all necessary dependencies. It installs all defined extras from `pyproject.toml`\n\n```bash\n./scripts/install-dev.sh\n```\n',
    'author': 'zerlok',
    'author_email': 'denergytro@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zerlok/asynchron',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
