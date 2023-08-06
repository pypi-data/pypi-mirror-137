# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyzoom']

package_data = \
{'': ['*']}

install_requires = \
['attrs',
 'cachetools>=4.1.0,<5.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'pyjwt>=2.0,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'shortuuid>=1.0.1,<2.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'pyzoom',
    'version': '0.1.13',
    'description': 'Python wrapper for Zoom Video API',
    'long_description': '![Zoom Logo](https://d24cgw3uvb9a9h.cloudfront.net/static/93946/image/new/ZoomLogo.png)\n\n# Python wrapper for Zoom API\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyzoom)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI](https://img.shields.io/pypi/v/pyzoom)](https://pypi.org/project/pyzoom/)\n![PyPI - License](https://img.shields.io/pypi/l/pyzoom)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/pyzoom)\n[![](https://img.shields.io/badge/Support-Buy_coffee!-Orange)](https://www.buymeacoffee.com/licht1stein)\n\nThis library is work in progress, and that includes documentation. Not all of the implemented methods are documented here,\nso please explore the `ZoomClient` class.\n\nLinks:\n* [Api Reference](https://marketplace.zoom.us/docs/api-reference)\n* [Using Zoom API](https://marketplace.zoom.us/docs/api-reference/using-zoom-apis)\n\n## Installation\n\nUsing pip:\n\n`pip install -U pyzoom`\n\nUsing [poetry](https://python-poetry.org/):\n\n`poetry add pyzoom`\n\n## Usage\n\n### Basic instantiation:\n\n```python\nfrom pyzoom import ZoomClient\n\nclient = ZoomClient(\'YOUR_ZOOM_API_KEY\', \'YOUR_ZOOM_API_SECRET\')\n```\n\n### Instantiation from environment variables\n\nYou can also create an instance of client when storing your key and secret in environment variables `ZOOM_API_KEY` \nand `ZOOM_API_SECRET`.\n\n```python\nfrom pyzoom import ZoomClient\n\nclient = ZoomClient.from_environment()\n```\n\n\n### Meetings\n\n#### Create meeting, update meeting and add registrant\n```python\nfrom pyzoom import ZoomClient\nfrom datetime import datetime as dt\n\nclient = ZoomClient.from_environment()\n\n# Creating a meeting\nmeeting = client.meetings.create_meeting(\'Auto created 1\', start_time=dt.now().isoformat(), duration_min=60, password=\'not-secure\')\n\n# Update a meeting\nmeeting = client.meetings.update_meeting(\'Auto updated 1\', meeting_id = meeting.id ,start_time=dt.now().isoformat(), duration_min=60,password=\'not-secure\')\n\n# Adding registrants\nclient.meetings.add_meeting_registrant(meeting.id, first_name=\'John\', last_name=\'Doe\', email=\'john.doe@example.com\')\n```\nYou can use `client.meetings.add_and_confirm_registrant` to also confirm auto added\nregistrants to a closed meeting.\n\n### Raw API methods\n\nYou can also use the library for making raw requests to the API:\n\n```python\nfrom pyzoom import ZoomClient\n\nclient = ZoomClient.from_environment()\n\n# Get self\nresponse = client.raw.get(\'/me\')\n\n# Get all pages of meeting participants\nresult_dict = client.raw.get_all_pages(\'/past_meetings/{meetingUUID}/participants\')\n```\n\n### Packaging notice\nThis project uses the excellent [poetry](https://python-poetry.org) for packaging. Please read about it and let\'s all start using\n`pyproject.toml` files as a standard. Read more:\n\n* [PEP 518 -- Specifying Minimum Build System Requirements for Python Projects](https://www.python.org/dev/peps/pep-0518/)\n\n* [What the heck is pyproject.toml?](https://snarky.ca/what-the-heck-is-pyproject-toml/)\n\n* [Clarifying PEP 518 (a.k.a. pyproject.toml)](https://snarky.ca/clarifying-pep-518/)\n\n\n### Support\n\n<a href="https://www.buymeacoffee.com/licht1stein" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" style="height: 30px !important;width: 130px !important;" ></a>\n\n### Disclaimer\nThis library is not related to Zoom Video Communications, Inc. It\'s an open-source project that \naims to simplify working with this suddenly very popular service.\n',
    'author': 'MB',
    'author_email': 'mb@blaster.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/licht1stein/pyzoom',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
