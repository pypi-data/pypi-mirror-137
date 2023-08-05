# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventsourcing_django', 'eventsourcing_django.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2.24,<5.0', 'eventsourcing[crypto]>=9.2.0,<9.3.0']

setup_kwargs = {
    'name': 'eventsourcing-django',
    'version': '0.2.0',
    'description': 'Python package for eventsourcing with Django.',
    'long_description': '# Event Sourcing with Django\n\nThis package supports using the Python\n[eventsourcing](https://github.com/pyeventsourcing/eventsourcing) library\nwith [Django ORM](https://www.djangoproject.com/).\n\nTo use Django with your Python eventsourcing applications:\n* install the Python package `eventsourcing_django`\n* add `\'eventsourcing_django\'` to your Django project\'s `INSTALLED_APPS` setting\n* migrate your database for this Django app\n* set the environment variable `PERSISTENCE_MODULE` to `\'eventsourcing_django\'`\n\nSee below for more information.\n\n\n## Installation\n\nUse pip to install the [stable distribution](https://pypi.org/project/eventsourcing_django/)\nfrom the Python Package Index. Please note, it is recommended to\ninstall Python packages into a Python virtual environment.\n\n    $ pip install eventsourcing_django\n\n\n## Django\n\nIf you are using Django 3.2 or later, add `\'eventsourcing_django\'`\nto your Django project\'s `INSTALLED_APPS` setting.\n\n    INSTALLED_APPS = [\n        ...\n        \'eventsourcing_django\',\n    ]\n\nIf you are using Django 2.2, 3.0 or 3.1, please add\n`\'eventsourcing_django.apps.EventsourcingConfig\'` to your Django\nproject\'s `INSTALLED_APPS` setting.\n\n    INSTALLED_APPS = [\n        ...\n        \'eventsourcing_django.apps.EventsourcingConfig\',\n    ]\n\n\nTo migrate your database, please run Django\'s `manage.py migrate` command.\n\n    $ python manage.py migrate eventsourcing_django\n\n\n## Event sourcing\n\nDefine aggregates and applications in the usual way.\n\n```python\nfrom eventsourcing.application import Application\nfrom eventsourcing.domain import Aggregate, event\nfrom uuid import uuid5, NAMESPACE_URL\n\n\nclass TrainingSchool(Application):\n    def register(self, name):\n        dog = Dog(name)\n        self.save(dog)\n\n    def add_trick(self, name, trick):\n        dog = self.repository.get(Dog.create_id(name))\n        dog.add_trick(trick)\n        self.save(dog)\n\n    def get_tricks(self, name):\n        dog = self.repository.get(Dog.create_id(name))\n        return dog.tricks\n\n\nclass Dog(Aggregate):\n    @event(\'Registered\')\n    def __init__(self, name):\n        self.name = name\n        self.tricks = []\n\n    @staticmethod\n    def create_id(name):\n        return uuid5(NAMESPACE_URL, f\'/dogs/{name}\')\n\n    @event(\'TrickAdded\')\n    def add_trick(self, trick):\n        self.tricks.append(trick)\n```\nConstruct and use the application in the usual way.\nSet `PERSISTENCE_MODULE` to `\'eventsourcing_django\'`\nin the application\'s environment.\nYou may wish to construct the application object on a signal\nwhen the Django project is "ready". You can use the `ready()`\nmethod of the `AppConfig` class in the `apps.py` module of a\nDjango app.\n\n```python\nschool = TrainingSchool(env={\n    "PERSISTENCE_MODULE": "eventsourcing_django",\n})\n```\n\nThe application\'s methods may be called from Django views and forms.\n\n```python\nschool.register(\'Fido\')\nschool.add_trick(\'Fido\', \'roll over\')\nschool.add_trick(\'Fido\', \'play dead\')\ntricks = school.get_tricks(\'Fido\')\nassert tricks == [\'roll over\', \'play dead\']\n```\n\nFor more information, please refer to the Python\n[eventsourcing](https://github.com/johnbywater/eventsourcing) library\nand the [Django](https://www.djangoproject.com/) project.\n',
    'author': 'John Bywater',
    'author_email': 'john.bywater@appropriatesoftware.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://eventsourcing.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
