# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bdantic', 'bdantic.models']

package_data = \
{'': ['*']}

install_requires = \
['beancount-stubs>=0.1.3,<0.2.0',
 'beancount>=2.3.4,<3.0.0',
 'jmespath>=0.10.0,<0.11.0',
 'orjson>=3.6.6,<4.0.0',
 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'bdantic',
    'version': '0.2.0',
    'description': 'A package for extending beancount with pydantic',
    'long_description': '# bdantic\n\n<p align="center">\n    <a href="https://github.com/jmgilman/bdantic/actions/workflows/ci.yml">\n        <img src="https://github.com/jmgilman/bdantic/actions/workflows/ci.yml/badge.svg"/>\n    </a>\n    <a href="https://pypi.org/project/bdantic">\n        <img src="https://img.shields.io/pypi/v/bdantic"/>\n    </a>\n</p>\n\n> A package for extending [beancount][1] with [pydantic][2]\n\nSee the [docs](https://jmgilman.github.io/bdantic/) for more details.\n\n## Installation\n\n```shell\npip install bdantic\n```\n\n## Usage\n\n### Parsing\n\nA handful of functions are provided for parsing Beancount types, but the primary\nmethod supports parsing most core types:\n\n```python\nimport bdantic\n\nfrom beancount.core import amount\nfrom decimal import Decimal\n\namt = amount.Amount(number=Decimal(1.50), currency="USD"))\nmodel = bdantic.parse(amt) # Produces a bdantic.models.Amount\n```\n\n### Exporting\n\nAll models can be directly exported back to their native Beancount types by\nusing their bult-in `export` method:\n\n```python\namt_export = model.export()\nassert amt == amt_export\n```\n\n### Ingesting\n\nFunctions are available for parsing common responses from interacting with the\nBeancount package. You can parse an entire Beancount file with the following:\n\n```python\nimport bdantic\n\nfrom beancount import loader\n\n# A bdantic.models.BeancountFile instance\nbfile = bdantic.parse_loader(*loader.load_file("ledger.beancount"))\nprint(len(bfile.entries))\n```\n\nYou can also parse the response from executing a query:\n\n```python\nimport bdantic\n\nfrom beancount import loader\nfrom beancount.query import query\n\nentries, _, options = loader.load_file("ledger.beancount")\n\nquery = "SELECT date, narration, account, position"\nresult = query.run_query(entries, options, query)\nparsed_result = bdantic.parse_query(result)\n```\n\nOr the result of running a realization:\n\n```python\nimport bdantic\n\nfrom beancount.core import realization\n\nentries, _, options = loader.load_file("ledger.beancount")\n\nreal = realization.realize(entries)\nparsed_real = bdantic.parse(real)\n```\n\n### Rendering\n\nPerhaps the most powerful usage of `bdantic` is rendering beancount data into a\nmore universal format like JSON. Since all models inherit from `Pydantic` they\ninclude full support for rendering their contents as JSON:\n\n```python\nimport bdantic\n\nfrom beancount import loader\n\nbfile = bdantic.parse_loader(*loader.load_file("ledger.beancount"))\njs = bfile.json()\nprint(js) # Look ma, my beancount data in JSON!\n```\n\nThe rendered JSON can be parsed back into the Beancount model that generated it:\n\n```python\nfrom bdantic.models import BeancountFile\n\nbfile = BeancountFile.parse_raw(js)\n```\n\nIn additiona to JSON, the directive models can be rendered as valid Beancount\nsyntax using the built-in `syntax` method:\n\n```python\nfrom bdantic.models import Amount, Posting, Transaction\nfrom datetime import date\nfrom decimal import Decimal\n\ntxn = Transaction(\n    date=date.today(),\n    meta={},\n    flag="*",\n    payee="Home Depot",\n    narration="Tools n stuff",\n    tags=None,\n    links=None,\n    postings=[\n        Posting(\n            account="Assets:Bank:Cash",\n            units=Amount(number=Decimal(-142.32), currency="USD"),\n            cost=None,\n            CostSpec=None,\n            flag=None,\n            meta={},\n        ),\n        Posting(\n            account="Expenses:HomeDepot",\n            units=Amount(number=Decimal(142.32), currency="USD"),\n            cost=None,\n            CostSpec=None,\n            flag=None,\n            meta={},\n        ),\n    ],\n)\n\nprint(txn.syntax())\n```\n\n## Testing\n\n```shell\npytest .\n```\n\nMost tests make heavy use of [hypothesis][3] for generating test data to be\nused in the tests. Hypothesis automatically keeps a cache to speed up subsequent\ntesting, however, the first time you run `pytest` you may experience longer than\nnormal run times.\n\nAdditionally, many tests pull from the `static.beancount` file found in the\ntesting folder. This was generated using the `bean-example` CLI tool and is used\nto verify models with a realistic ledger.\n\n## Contributing\n\nCheck out the [issues][4] for items needing attention or submit your own and\nthen:\n\n1. [Fork the repo][5]\n2. Create your feature branch (git checkout -b feature/fooBar)\n3. Commit your changes (git commit -am \'Add some fooBar\')\n4. Push to the branch (git push origin feature/fooBar)\n5. Create a new Pull Request\n\n[1]: https://github.com/beancount/beancount\n[2]: https://github.com/samuelcolvin/pydantic\n[3]: https://hypothesis.readthedocs.io/en/latest/\n[4]: https://github.com/jmgilman/bdantic/issues\n[5]: https://github.com/jmgilman/bdantic/fork\n',
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
