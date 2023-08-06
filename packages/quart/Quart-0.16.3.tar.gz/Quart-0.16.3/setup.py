# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['quart', 'quart.flask_patch', 'quart.json', 'quart.testing', 'quart.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles',
 'blinker',
 'click',
 'hypercorn>=0.11.2',
 'itsdangerous',
 'jinja2',
 'toml',
 'werkzeug>=2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata', 'typing_extensions'],
 'dotenv': ['python-dotenv']}

entry_points = \
{'console_scripts': ['quart = quart.cli:main']}

setup_kwargs = {
    'name': 'quart',
    'version': '0.16.3',
    'description': 'A Python ASGI web microframework with the same API as Flask',
    'long_description': 'Quart\n=====\n\n.. image:: https://assets.gitlab-static.net/pgjones/quart/raw/main/artwork/logo.png\n   :alt: Quart logo\n\n|Build Status| |docs| |pypi| |python| |license| |chat|\n\nQuart is an async Python web microframework. Using Quart you can,\n\n* render and serve HTML templates,\n* write (RESTful) JSON APIs,\n* serve WebSockets,\n* stream request and response data,\n* do pretty much anything over the HTTP or WebSocket protocols.\n\nQuickstart\n----------\n\nQuart can be installed via `pip\n<https://docs.python.org/3/installing/index.html>`_,\n\n.. code-block:: console\n\n    $ pip install quart\n\nand requires Python 3.7.0 or higher (see `python version support\n<https://pgjones.gitlab.io/quart/discussion/python_versions.html>`_ for\nreasoning).\n\nA minimal Quart example is,\n\n.. code-block:: python\n\n    from quart import Quart, render_template, websocket\n\n    app = Quart(__name__)\n\n    @app.route("/")\n    async def hello():\n        return await render_template("index.html")\n\n    @app.route("/api")\n    async def json():\n        return {"hello": "world"}\n\n    @app.websocket("/ws")\n    async def ws():\n        while True:\n            await websocket.send("hello")\n            await websocket.send_json({"hello": "world"})\n\n    if __name__ == "__main__":\n        app.run()\n\nif the above is in a file called ``app.py`` it can be run as,\n\n.. code-block:: console\n\n    $ python app.py\n\nTo deploy this app in a production setting see the `deployment\n<https://pgjones.gitlab.io/quart/tutorials/deployment.html>`_\ndocumentation.\n\nContributing\n------------\n\nQuart is developed on `GitLab <https://gitlab.com/pgjones/quart>`_. If\nyou come across an issue, or have a feature request please open an\n`issue <https://gitlab.com/pgjones/quart/issues>`_. If you want to\ncontribute a fix or the feature-implementation please do (typo fixes\nwelcome), by proposing a `merge request\n<https://gitlab.com/pgjones/quart/merge_requests>`_.\n\nTesting\n~~~~~~~\n\nThe best way to test Quart is with `Tox\n<https://tox.readthedocs.io>`_,\n\n.. code-block:: console\n\n    $ pip install tox\n    $ tox\n\nthis will check the code style and run the tests.\n\nHelp\n----\n\nThe Quart `documentation <https://pgjones.gitlab.io/quart/>`_ or\n`cheatsheet\n<https://pgjones.gitlab.io/quart/reference/cheatsheet.html>`_ are the\nbest places to start, after that try searching `stack overflow\n<https://stackoverflow.com/questions/tagged/quart>`_ or ask for help\n`on gitter <https://gitter.im/python-quart/lobby>`_. If you still\ncan\'t find an answer please `open an issue\n<https://gitlab.com/pgjones/quart/issues>`_.\n\nRelationship with Flask\n-----------------------\n\nQuart is an asyncio reimplementation of the popular `Flask\n<http://flask.pocoo.org/>`_ microframework API. This means that if you\nunderstand Flask you understand Quart.\n\nLike Flask Quart has an ecosystem of extensions for more specific\nneeds. In addition a number of the Flask extensions work with Quart.\n\nMigrating from Flask\n~~~~~~~~~~~~~~~~~~~~\n\nIt should be possible to migrate to Quart from Flask by a find and\nreplace of ``flask`` to ``quart`` and then adding ``async`` and\n``await`` keywords. See the `docs\n<https://pgjones.gitlab.io/quart/how_to_guides/flask_migration.html>`_\nfor more help.\n\n\n.. |Build Status| image:: https://gitlab.com/pgjones/quart/badges/main/pipeline.svg\n   :target: https://gitlab.com/pgjones/quart/commits/main\n\n.. |docs| image:: https://img.shields.io/badge/docs-passing-brightgreen.svg\n   :target: https://pgjones.gitlab.io/quart/\n\n.. |pypi| image:: https://img.shields.io/pypi/v/quart.svg\n   :target: https://pypi.python.org/pypi/Quart/\n\n.. |python| image:: https://img.shields.io/pypi/pyversions/quart.svg\n   :target: https://pypi.python.org/pypi/Quart/\n\n.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg\n   :target: https://gitlab.com/pgjones/quart/blob/main/LICENSE\n\n.. |chat| image:: https://img.shields.io/badge/chat-join_now-brightgreen.svg\n   :target: https://gitter.im/python-quart/lobby\n',
    'author': 'pgjones',
    'author_email': 'philip.graham.jones@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/pgjones/quart/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
