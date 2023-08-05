# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiobungie', 'aiobungie.crate', 'aiobungie.interfaces', 'aiobungie.internal']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp==3.8.1', 'attrs==21.4.0', 'python-dateutil==2.8.2']

setup_kwargs = {
    'name': 'aiobungie',
    'version': '0.2.5',
    'description': 'A Python and Asyncio API for Bungie.',
    'long_description': '<div align="center">\n    <h1>aiobungie</h1>\n    <p>An asynchronous statically typed API wrapper for the Bungie API written in Python.</p>\n    <a href="https://codeclimate.com/github/nxtlo/aiobungie/maintainability">\n    <img src="https://api.codeclimate.com/v1/badges/09e71a0374875d4594f4/maintainability"/>\n    </a>\n    <a href="https://github.com/nxtlo/aiobungie/issues">\n    <img src="https://img.shields.io/github/issues/nxtlo/aiobungie"/>\n    </a>\n    <a href="http://python.org">\n    <img src="https://img.shields.io/badge/python-3.9%20%7C%203.10-blue"/>\n    </a>\n    <a href="https://pypi.org/project/aiobungie/">\n    <img src="https://img.shields.io/pypi/v/aiobungie?color=green"/>\n    </a>\n    <a href="https://github.com/nxtlo/aiobungie/blob/master/LICENSE">\n    <img src="https://img.shields.io/pypi/l/aiobungie"/>\n    </a>\n    <a href="https://github.com/nxtlo/aiobungie/actions/workflows/ci.yml">\n    <img src="https://github.com/nxtlo/aiobungie/actions/workflows/ci.yml/badge.svg?branch=master">\n    </a>\n</div>\n\n# Installing\n\n_IT IS recommended_ to use the latest pre-release from master\nsince `0.2.4` is missing features from `0.2.5`.\n\n\nPyPI stable release. __Not Recommended Currently__.\n\n```sh\n$ pip install aiobungie\n```\n\nFrom master __Recommended Currently__.\n\n```sh\n$ pip install git+https://github.com/nxtlo/aiobungie\n```\n\n## Quick Example\n\nSee [Examples for advance usage.](https://github.com/nxtlo/aiobungie/tree/master/examples)\n\n```python\nimport aiobungie\n\n# crates in aiobungie are implementations\n# of Bungie\'s objects to provide\n# more functionality.\n\nclient = aiobungie.Client(\'YOUR_API_KEY\')\n\nasync def main() -> None:\n\n    # fetch a clan\n    clan: aiobungie.crate.Clan = await client.fetch_clan("Nuanceㅤ")\n    print(clan.name, clan.id)\n\n    # Clan owner.\n    if owner := clan.owner:\n\n        # Fetch a profile.\n        profile: aiobungie.crate.Component = await client.fetch_profile(\n            owner.id,\n            owner.type,\n            # Return All profile components and character components.\n            aiobungie.ComponentType.CHARACTERS,\n            *aiobungie.ComponentType.ALL_PROFILES.value\n            # If a method requires OAuth2 you may wanna pass an auth token as a kwarg.\n            auth="access_token"\n        )\n\n        # A profile characters component as a mapping from each character id to a character object.\n        if owner_characters := profile.characters:\n            for character_id, character in owner_characters.items():\n                print(f"ID: {character_id}: Character {character}")\n\n                # Check if warlock\n                if character.class_type is aiobungie.Class.WARLOCK:\n                    # Do something with the warlock\n                    ...\n\n# You can either run it using the client or just `asyncio.run(main())`\nclient.run(main())\n```\n\n## RESTful client\nAlternatively, You can use `RESTClient` which\'s designed to only make HTTP requests and return JSON objects.\n\n### Quick Example\n```py\nimport aiobungie\nimport asyncio\n\nasync def main(access_token: str) -> None:\n    # Max retries is the maximum retries to backoff when you hit 5xx error codes.\n    # It defaults to 4 retries.\n    async with aiobungie.RESTClient("TOKEN", max_retries=5) as rest:\n        # Passing the player\'s name and code -> \'Fate怒#4275\'\n        fetch_player = await rest.fetch_player(\'Fate怒\', 4275)\n        print(*fetch_player) # A JSON array of dict object\n        for player in fetch_player: # Iterate through the array.\n            print(player[\'membershipId\'], player[\'iconPath\']) # The player id and icon path.\n            for k, v in player.items():\n                print(k, v)\n\n            # You can also send your own requests.\n            await rest.static_request("POST", "Need/OAuth2", headers={"A-HEADER": f"A-Value"}, auth=access_token)\n            # Defined methods.\n            await rest.send_friend_request(access_token, member_id=1234)\n\nasyncio.run(main("DB_ACCESS_TOKEN"))\n```\n\n### Requirements\n* Python 3.9 or higher\n* aiohttp\n* attrs\n\n## Contributing\nPlease read this [manual](https://github.com/nxtlo/aiobungie/blob/master/CONTRIBUTING.md)\n\n### Getting Help\n* Discord: `Fate 怒#0008` | `350750086357057537`\n* Docs: [Here](https://nxtlo.github.io/aiobungie/).\n',
    'author': 'nxtlo',
    'author_email': 'dhmony-99@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nxtlo/aiobungie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
