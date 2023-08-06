# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['routerling']

package_data = \
{'': ['*']}

install_requires = \
['uvicorn>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'routerling',
    'version': '0.4.2',
    'description': 'Extremely Stupid Simple, Blazing Fast, Get Out of your way immediately Microframework for building Python Web Applications.',
    'long_description': '# Routerling : <img src="https://img.shields.io/badge/coverage-95%25-green" />\n\nRouterling is a very very small, extremely tiny, and insanely fast [ASGI](https://asgi.readthedocs.io) web application framework. It was designed to facilitate productivity by allowing for complete mastery in 7 minutes or less.\n\nRouterling is a very light layer around ASGI with support for application mounting and is perhaps the simplest and one of the fastest python web frameworks (biased opinion of course).\n\n\n## Installling\nInstall with [pip](https://pip.pypa.io/en/stable/getting-started/)\n```sh\n$ pip install routerling\n```\n\n## A Simple Example\n<hr/>\n\n```py\nfrom routerling import Router\n\n\nasync def index(req, res, ctx):\n    res.body = \'Hello, World!\'\n\n\nrouter = Router()\n\n\nrouter.GET(\'/\', index)\n```\n\nYou can run with uvicorn, gunicorn or any other asgi HTTP, HTTP2, and web socket protocol server of your choice.\n```sh\n$ uvicorn main:router --reload\n * Running on http://127.0.0.1:8000\n```\n\n\n## Contributing\n\nFor guidance on how to make contributions to Routerling, see the [Contribution Guidelines](contributions.md)\n\n\n## Links\n\n- Documentation [Go To Docs](https://rayattack.github.io/routerling)\n- PyPi [https://pypi.org/project/routerling](https://pypi.org/project/routerling)\n- Source Code [Github](https://github.com/rayattack/routerling)\n',
    'author': 'Raymond Ortserga',
    'author_email': 'ortserga@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
