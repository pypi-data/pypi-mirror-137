# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bdantic', 'bdantic.models']

package_data = \
{'': ['*']}

install_requires = \
['beancount-stubs>=0.1.1,<0.2.0',
 'beancount>=2.3.4,<3.0.0',
 'orjson>=3.6.6,<4.0.0',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'bdantic',
    'version': '0.1.0',
    'description': 'A package for extending beancount with pydantic',
    'long_description': '# bdantic\n\n<p align="center">\n    <a href="https://github.com/jmgilman/bdantic/actions/workflows/ci.yml">\n        <img src="https://github.com/jmgilman/bdantic/actions/workflows/ci.yml/badge.svg"/>\n    </a>\n    <a href="https://pypi.org/project/bdantic">\n        <img src="https://img.shields.io/pypi/v/bdantic"/>\n    </a>\n</p>\n\n> A package for extending [beancount][1] with [pydantic][2]\n\n## Install\n\n```shell\n$> pip install bdantic\n```\n\n## Usage\n\nThe package includes compatible models for all of the core beancount data types.\nModels are created by converting a beancount type into its respective model:\n\n```python\nfrom beancount.core import amount\nfrom bdantic import parse\nfrom decimal import Decimal\n\namt = amount.Amount(number=Decimal(1.50), currency="USD"))\nmodel = parse(amt) # Produces a bdantic.models.Amount\n```\n\nAll models can be exported back into their original beancount data type:\n\n```python\namt_export = model.export()\nassert amt == amt_export # The exported object is identical to the original\n```\n\nSince all models are Pydantic base models, it\'s possible to export the entire\nresult of parsing a beancount file into JSON:\n\n```python\nfrom beancount import loader\nfrom bdantic import parse_loader\n\nresult = parse_loader(*loader.load_file("testing/static.beancount"))\n\nprint(result.json())\n```\n\nNote that models are not compatible with beancount functions as most functions\nmake heavy use of type checking and will fail when passed a model. It\'s expected\nto do all processing using the beancount package and then convert the types to\nmodels when needed. Additionally, while JSON can be generated, it\'s not\nguaranteed to go both ways due to limitations with Pydantic type coercion:\n\n```python\nfrom bdantic.models import BeancountFile\n\n# Should work in most cases\nbeancount_file = BeancountFile.parse_raw(result.json())\n```\n\n## Contributing\n\nCheck out the [issues][3] for items needing attention or submit your own and\nthen:\n\n1. [Fork the repo][4]\n2. Create your feature branch (git checkout -b feature/fooBar)\n3. Commit your changes (git commit -am \'Add some fooBar\')\n4. Push to the branch (git push origin feature/fooBar)\n5. Create a new Pull Request\n\n[1]: https://github.com/beancount/beancount\n[2]: https://github.com/samuelcolvin/pydantic\n[3]: https://github.com/jmgilman/bdantic/issues\n[4]: https://github.com/jmgilman/bdantic/fork\n',
    'author': 'Joshua Gilman',
    'author_email': 'joshuagilman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmgilman/bdantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
