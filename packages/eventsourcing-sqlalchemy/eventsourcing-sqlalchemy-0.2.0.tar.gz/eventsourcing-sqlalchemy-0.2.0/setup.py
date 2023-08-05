# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventsourcing_sqlalchemy']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy-Utils>=0.38.2,<0.39.0',
 'SQLAlchemy>=1.4.26,<1.5.0',
 'eventsourcing[crypto]>=9.2.0,<9.3.0']

setup_kwargs = {
    'name': 'eventsourcing-sqlalchemy',
    'version': '0.2.0',
    'description': 'Python package for eventsourcing with SQLAlchemy.',
    'long_description': '# Event Sourcing in Python with SQLAlchemy\n\nThis package supports using the Python\n[eventsourcing](https://github.com/pyeventsourcing/eventsourcing) library\nwith [SQLAlchemy](https://www.sqlalchemy.org/).\n\nTo use SQLAlchemy with your Python eventsourcing applications:\n* install the Python package `eventsourcing_sqlalchemy`\n* set the environment variable `PERSISTENCE_MODULE` to `\'eventsourcing_sqlalchemy\'`\n* set the environment variable `SQLALCHEMY_URL` to an SQLAlchemy database URL\n\nSee below for more information.\n\n## Installation\n\nUse pip to install the [stable distribution](https://pypi.org/project/eventsourcing_sqlalchemy/)\nfrom the Python Package Index. Please note, it is recommended to\ninstall Python packages into a Python virtual environment.\n\n    $ pip install eventsourcing_sqlalchemy\n\n## Getting started\n\nDefine aggregates and applications in the usual way.\n\n```python\nfrom eventsourcing.application import Application\nfrom eventsourcing.domain import Aggregate, event\nfrom uuid import uuid5, NAMESPACE_URL\n\n\nclass TrainingSchool(Application):\n    def register(self, name):\n        dog = Dog(name)\n        self.save(dog)\n\n    def add_trick(self, name, trick):\n        dog = self.repository.get(Dog.create_id(name))\n        dog.add_trick(trick)\n        self.save(dog)\n\n    def get_tricks(self, name):\n        dog = self.repository.get(Dog.create_id(name))\n        return dog.tricks\n\n\nclass Dog(Aggregate):\n    @event(\'Registered\')\n    def __init__(self, name):\n        self.name = name\n        self.tricks = []\n\n    @staticmethod\n    def create_id(name):\n        return uuid5(NAMESPACE_URL, f\'/dogs/{name}\')\n\n    @event(\'TrickAdded\')\n    def add_trick(self, trick):\n        self.tricks.append(trick)\n```\n\nTo use this module as the persistence module for your application, set the environment\nvariable `PERSISTENCE_MODULE` to `\'eventsourcing_sqlalchemy\'`.\n\nWhen using this module, you need to set the environment variable `SQLALCHEMY_URL` to an\nSQLAlchemy database URL for your database.\nPlease refer to the [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/14/core/engines.html)\nfor more information about SQLAlchemy Database URLs.\n\n```python\nimport os\n\nos.environ["PERSISTENCE_MODULE"] = "eventsourcing_sqlalchemy"\nos.environ["SQLALCHEMY_URL"] = "sqlite:///:memory:"\n```\n\nConstruct and use the application in the usual way.\n\n```python\nschool = TrainingSchool()\nschool.register(\'Fido\')\nschool.add_trick(\'Fido\', \'roll over\')\nschool.add_trick(\'Fido\', \'play dead\')\ntricks = school.get_tricks(\'Fido\')\nassert tricks == [\'roll over\', \'play dead\']\n```\n\nSee the library\'s [documentation](https://eventsourcing.readthedocs.io/)\nand the [SQLAlchemy](https://www.sqlalchemy.org/) project for more information.\n',
    'author': 'John Bywater',
    'author_email': 'john.bywater@appropriatesoftware.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://eventsourcing.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
