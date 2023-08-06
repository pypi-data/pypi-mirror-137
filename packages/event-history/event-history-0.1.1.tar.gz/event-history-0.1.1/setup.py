# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['event_history']

package_data = \
{'': ['*']}

modules = \
['LICENSE']
setup_kwargs = {
    'name': 'event-history',
    'version': '0.1.1',
    'description': 'A minimal library to work with versioned events in atomic database transactions.',
    'long_description': '# Even History\n\n## Why do we need this?\n\nWell, you probably don\'t. But I needed it for something personal that I was working on and thought\nit would be good to show it off so that maybe it can help someone else.\n\n## Usecases\n\nThe library is quite simple, you only have to have two classes that satisfy\nthe `IEventHistoryService` and `IEventService` protocols.\n\nThe `IEventHistoryService` is a simple protocol, that has a `save` method which\ntakes in only two arguments, one the object its trying to save, called `event_object`\n\n(NOTE its not a keyword argument in the `TransactionService` so the first position\nargument would be expected to be event_object.) The `IEventService` protocol is very\nsimilar to it and has two methods, `save` and `update` methods. Both of which have the\nsame calling signature, the first argument is `event_object` which is the object that\nyou want to save and the other arugment is a keyword argument called `session` .\n\nThe `session` is the `ContextManager` provided by many database library for\nACID transactions. PyMongo provides it too, using the `start_session` method of\n`pymongo.MongoClient` class.\n\n## What does it do\n\nThis library is very simple, in fact quite a dumb one to begin with but it does\nits simple job well. The idea is to use the already existing services with your\nbusiness entity (models). The requirement for this library is quite simple too, all\nyou need is a service layer to save and update date in your desired database.\nYou would also need a context manager, either make one yourself (refer to the `tests`\n\ndirectory to see how to make a simple one) or use the one provided with your database\ndrivers/library.\n\nAfter which, all you need to do is to initialise the `TransactionService` class with\nthese services as arguments.\n\nFor example, \n\n```python\n...\n\n@dataclasses.dataclass\nclass Event:\n    ...\n    # these two are required fields to be included in\n    # your model for TransactionService to work properly.\n    timestampt: datetime.datetime\n    version: int = 0\n\nclass EventService:\n    ...\n\n    def save(self, event_object, session=None):\n        ...\n\n    def update(self, event_object, session=None):\n        ...\n\nclass EventHistoryService:\n    ...\n\n    def save(self, event_object, session=None):\n        ...\n\nclient = pymongo.MongoClient("url-to-some-replica-set")\n\nyour_event_object = Event(**some_data_dict)\n\ntransaction_service = event_history.TransactionService(\n    EventService(),\n    EventHistoryService(),\n)\n\nwith client.start_session() as session:\n    transaction_service.save(your_event_object, session=session)\n\nlogging.info("All done! Now check your database.")\n\n...\n\nyour_event_object = Event(**some_updated_dict)\n\nwith client.start_session() as session:\n    transaction_service.update(your_event_object, session=session)\n\nloggin.info("It should be updated! Now check your database.)\n\n```\n\nThis is a minimal example that shows that basic use of this Transaction service with\nPyMongo sessions but as explained earlier, this library is designed to be context\nagnostic and can handler it with any context manager you provide (as long as your\n`save` and `update` methods in service classes is able to use them).\n\n---\n\nFinally, you can use this library if you want - however, I don\'t think this is an\nactual library since all its doing is abstracting away some of the burden of writing\nfurther abstractions on top of your service layers. So, if you can just look at\nthe pattern and come up with your own simple abstraction, that would be better than\nadding a dependency (this sideproject) in your projects.\n\nFor a fully fledged example, take a look at the `example` directory and the code inside.\nIt shows how it can be used with `pymongo` library and how it can work very nicely\nwith it.\n',
    'author': 'Taj',
    'author_email': 'tjgurwara99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tjgurwara99/event-history',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
