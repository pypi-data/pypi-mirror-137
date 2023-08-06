# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crescent', 'crescent.commands', 'crescent.internal', 'crescent.utils']

package_data = \
{'': ['*'], 'crescent': ['components/*']}

install_requires = \
['attrs>=21.4.0,<22.0.0', 'hikari>=2.0.0.dev106']

setup_kwargs = {
    'name': 'hikari-crescent',
    'version': '0.1.0b1',
    'description': '🌕 A dead simple command handler for Hikari',
    'long_description': '# hikari-crescent\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/magpie-dev/hikari-crescent/main.svg)](https://results.pre-commit.ci/latest/github/magpie-dev/hikari-crescent/main)\n\nA simple command handler for [Hikari](https://github.com/hikari-py/hikari).\n\n## Features\n - Simple and intuitive API.\n - Slash, user, and message commands.\n - Error handling.\n\n## Installation\nCrescent is supported in python3.8+.\n```\npip install hikari-crescent\n````\n\n\n## Usage\nCrescent uses signature parsing to generate your commands. Creating commands is as easy as adding typehints!\n\n```python\nimport crescent\n\nbot = crescent.Bot("YOUR_TOKEN")\n\n# Include the command in your bot - don\'t forget this\n@bot.include\n# Create a slash command\n@crescent.command\nasync def say(ctx: crescent.Context, word: str):\n    await ctx.respond(word)\n\nbot.run()\n```\n\nInformation for arguments can be provided using the `Annotated` type hint.\nSee [this example](https://github.com/magpie-dev/hikari-crescent/blob/main/examples/basic/basic.py) for more information.\n\n```python\n# python 3.9 +\nfrom typing import Annotated as Atd\n\n# python 3.8\nfrom typing_extensions import Annotated as Atd\n\n@bot.include\n@crescent.command\nasync def say(ctx: crescent.Context, word: Atd[str, "The word to say"]):\n    await ctx.respond(word)\n```\n\nCommands can also be inside of a sublcassed `crescent.Bot` object for an object-oriented workflow.\n\n```python\n\nimport crescent\n\nclass Bot(crescent.Bot):\n\n    # bot.include isn\'t needed in subclasses!\n    @crescent.command\n    async def say(self, ctx: crescent.Context, word: str):\n        await ctx.respond(word)\n\n```\n\n\n# Support\n\nContact `Lunarmagpie❤#0001` on Discord or create an issue. All questions are welcome!\n\n# Contributing\n\nCreate a issue for your feature. There aren\'t any guildlines right now so just don\'t be rude.\n',
    'author': 'Lunarmagpie',
    'author_email': 'Bambolambo0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
