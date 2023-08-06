# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gke_logging']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0']

extras_require = \
{'asgi': ['starlette>=0.18.0,<0.19.0']}

setup_kwargs = {
    'name': 'gke-logging',
    'version': '0.0.3',
    'description': 'Utilities for interacting with logging facilities in GKE workloads',
    'long_description': '# gke-logging\n\n[![PyPI version](https://badge.fury.io/py/gke-logging.svg)](https://badge.fury.io/py/gke-logging)\n\nUtilities for interacting with logging facilities in GKE workloads\n\n## Installation\n\n### Requirements\n\n- Python 3.7+\n- [Poetry](https://python-poetry.org/) (for development only)\n\n### Install from PyPI (recommended)\n\n```\npip install gke-logging\n```\n\n### Installing from Github\n\n```\npip install git+https://github.com/StationA/gke-logging.git#egg=gke-logging\n```\n\n### Installing from source\n\n```\ngit clone https://github.com/StationA/gke-logging.git\ncd gke-logging\npoetry install\n```\n\n## Usage\n\n### `gke_logging.GKELoggingFormatter`\n\nOne of the core components is the `GKELoggingFormatter`, which is an implementation of the built-in\n`logging.Formatter` protocol that translates a `logging.LogRecord` into a JSON format that GKE\'s\nlogging infrastructure can understand. At a minimum, this enables any software running on GKE to\nintegrate structured logging simply by applying this formatter for your loggers, e.g.:\n\n```python\nimport logging\n\nfrom gke_logging import GKELoggingFormatter\n\n\nLOGGER = logging.getLogger(__name__)\nh = logging.StreamHandler()\nh.setFormatter(GKELoggingFormatter())\nLOGGER.addHandler(h)\nLOGGER.setLevel(logging.INFO)\n\n\n# ...\n\nLOGGER.info("Look at me! I can haz GKE structured logging!")\n# Prints out: {"time": "2022-01-13T23:22:26.336686+00:00", "severity": "INFO", "message": "Look at me! I can haz GKE structured logging!", "logging.googleapis.com/sourceLocation": {"file": "test_log.py", "line": "14", "function": "<module>"}, "logging.googleapis.com/labels": {}}\n```\n\nFurthermore, this formatter allows you to set app-level metadata to be sent along with each log\nmessage, which is useful in order to better organize collected log data:\n\n```python\n# ...\nh.setFormatter(\n    GKELoggingFormatter(default_labels=dict(app_id="my-cool-app", version="0.1.0"))\n)\n# ...\n```\n\nAlso the formatter also allows you to add HTTP metadata to any logs that occur during the course of\na request. This enhances logs that are emitted during request-handling logic in APIs with additional\ndata. This functionality is primarily utilized in the included `GKELoggingMiddleware` in order to\nprovide basic access logs.\n\n### `gke_logging.asgi.GKELoggingMiddleware`\n\n`gke_logging.asgi.GKELoggingMiddleware` is an ASGI middleware that emits basic access logs in\n"common log format", with a default behavior that integrates with the `GKELoggingFormatter` to write\nthe access logs in a format that GKE\'s logging infrastructure better understands. By implementing\nper the ASGI spec, this means it can work with any ASGI-compatible server, including FastAPI,\nstarlette, and ASGI implementations:\n\n```python\nfrom fastapi import FastAPI\nfrom gke_logging.asgi import GKELoggingMiddleware\n\napp = FastAPI()\napp.add_middleware(GKELoggingMiddleware)\n\n@app.get("/")\ndef get_it() -> str:\n    return "OK"\n```\n\nAdditionally, because this middleware integrates with `gke_logging.context` bindings, it enables any\nlogger used during the course of handling a request to emit logs that also contain request-time\ndata, e.g. request URL, user-agent, response latency, etc.\n\n```python\nimport logging\n\nfrom fastapi import FastAPI\nfrom gke_logging import GKELoggingFormatter\nfrom gke_logging.asgi import GKELoggingMiddleware\n\napp = FastAPI()\napp.add_middleware(GKELoggingMiddleware)\n\n\nroot_logger = logging.getLogger()\nh = logging.StreamHandler()\nh.setFormatter(GKELoggingFormatter())\nroot_logger.setLevel(logging.INFO)\nroot_logger.addHandler(h)\n\n\n@app.get("/")\ndef get_it() -> str:\n    # Any log records created during request-handling will be enriched with other HTTP request data\n    root_logger.info("TEST")\n    return "OK"\n```\n\n### `gke_logging.context`\n\nIn order to control additional metadata labels for log records that correspond to one logical\noperation, e.g. an HTTP request, a batch job operation, etc., you should use the helper functions\nexported in `gke_logging.context`:\n\n```python\nimport logging\n\nfrom contextvars import copy_context\n\nfrom gke_logging import GKELoggingFormatter\nfrom gke_logging.context import set_labels\n\n\nLOGGER = logging.getLogger(__name__)\nh = logging.StreamHandler()\nh.setFormatter(GKELoggingFormatter())\nLOGGER.addHandler(h)\nLOGGER.setLevel(logging.INFO)\n\n# ...\n\n\ndef run_job(job_id: str):\n    set_labels(job_id=job_id)\n    LOGGER.info("TEST")\n\n\nctx = copy_context()\nfor i in range(10):\n    ctx.run(run_job, f"{i + 1}")\n```\n\nBecause `ContextVar`s bind natively to Python\'s `asyncio`, you can use these same helper\nfunctions within asynchronous tasks in a similar fashion.\n\n### Additional examples\n\nAdditional usage examples can be found in [examples/](examples/)\n\n## Contributing\n\nWhen contributing to this repository, please follow the steps below:\n\n1. Fork the repository\n1. Submit your patch in one commit, or a series of well-defined commits\n1. Submit your pull request and make sure you reference the issue you are addressing\n',
    'author': 'Station A',
    'author_email': 'oss@stationa.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
