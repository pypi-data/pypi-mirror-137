# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grobid_client',
 'grobid_client.api',
 'grobid_client.api.pdf',
 'grobid_client.models']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.1.0,<22.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'httpx>=0.15.4,<0.23.0',
 'lxml>=4.7.1,<5.0.0',
 'python-dateutil>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'grobid-client',
    'version': '0.7.7',
    'description': 'A client library for accessing Grobid',
    'long_description': '# grobid-client\nA client library for accessing [Grobid](https://github.com/kermitt2/grobid)\n\n## Usage\nFirst, create a client:\n\n```python\nfrom grobid_client import Client\n\nclient = Client(base_url="https://cloud.science-miner.com/grobid/api")\n```\n\nNow call your endpoint and use your models:\n\n```python\nfrom pathlib import Path\nfrom grobid_client.api.pdf import process_fulltext_document\nfrom grobid_client.models import Article, ProcessForm\nfrom grobid_client.types import TEI, File\npdf_file = "MyPDFFile.pdf"\nwith pdf_file.open("rb") as fin:\n    form = ProcessForm(\n        segment_sentences="1",\n        input_=File(file_name=pdf_file.name, payload=fin, mime_type="application/pdf),\n    )\n    r = process_fulltext_document.sync_detailed(client=client, multipart_data=form)\n    if r.is_success:\n        article: Article = TEI.parse(r.content, sentences=True, figures=False)\n        assert article.title\n\n```\n\nThings to know:\n1. Every path/method combo becomes a Python module with four functions:\n    1. `sync`: Blocking request that returns parsed data (if successful) or `None`\n    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.\n    1. `asyncio`: Like `sync` but the async instead of blocking\n    1. `asyncio_detailed`: Like `sync_detailed` by async instead of blocking\n\n1. All path/query params, and bodies become method arguments.\n1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)\n1. Any endpoint which did not have a tag will be in `entifyfishing_client.api.default`\n\n## Building / publishing this Client\nThis project uses [Poetry](https://python-poetry.org/) to manage dependencies  and packaging.  Here are the basics:\n1. Update the metadata in pyproject.toml (e.g. authors, version)\n1. If you\'re using a private repository, configure it with Poetry\n    1. `poetry config repositories.<your-repository-name> <url-to-your-repository>`\n    1. `poetry config http-basic.<your-repository-name> <username> <password>`\n1. Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI, just `poetry publish --build`\n\nIf you want to install this client into another project without publishing it (e.g. for development) then:\n1. If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project\n1. If that project is not using Poetry:\n    1. Build a wheel with `poetry build -f wheel`\n    1. Install that wheel from the other project `pip install <path-to-wheel>`\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
