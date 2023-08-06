# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moe',
 'moe.library',
 'moe.plugins',
 'moe.plugins.add',
 'moe.plugins.add.add_core',
 'moe.plugins.edit',
 'moe.plugins.moe_import',
 'moe.plugins.move',
 'moe.plugins.musicbrainz',
 'moe.plugins.remove']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy[mypy]>=1.4.15,<2.0.0',
 'Unidecode>=1.2.0,<2.0.0',
 'alembic>=1.4.2,<2.0.0',
 'dynaconf>=3.1.4,<4.0.0',
 'mediafile>=0.6.0,<0.7.0',
 'musicbrainzngs>=0.7.1,<0.8.0',
 'pluggy>=0.13.1,<0.14.0',
 'pyyaml>=5.3.1,<6.0.0',
 'questionary>=1.9.0,<2.0.0']

extras_require = \
{'docs': ['furo>=2021.7.5-beta.38,<2022.0.0', 'Sphinx>=4.0.2,<5.0.0']}

entry_points = \
{'console_scripts': ['moe = moe.cli:main']}

setup_kwargs = {
    'name': 'moe',
    'version': '0.8.2',
    'description': 'The ultimate tool for managing your music library.',
    'long_description': "###############\nWelcome to Moe!\n###############\nMoe is our resident Music-Organizer-Extraordinaire who's sole purpose is to give you full control over your music library. In other words, it's a commandline-interface for managing your music.\n\n*******************\nDevelopment Warning\n*******************\nMoe is currently in early development, and is still training for his goal to become your all-powerful music library assistant. You are more than welcome to start using Moe, but don't be surprised if you find any bugs or a lack of features. If you do find any bugs, or would like to request a feature, please feel free to `open an issue <https://github.com/MoeMusic/Moe/issues/new/choose>`_.\n\nSo what can Moe do right now?\n=============================\n* Add music to your library, fixing tags with metadata from Musicbrainz.\n* Organize, remove, list, and edit your music in the library.\n* Supports including extra files with an album e.g. log or playlist files.\n* Supports tags with multiple values.\n\nIf you want to learn more, check out the `Getting Started <https://mrmoe.readthedocs.io/en/latest/getting_started.html>`_ docs.\n\n********\nWhy Moe?\n********\nMoe takes *a lot* of inspiration from `beets <https://github.com/beetbox/beets>`_. If you haven't checked it out, please do so. It's an extremely impressive piece of software and `Adrian <https://github.com/sampsyo>`_ has done a great job developing it over the years. If you're looking for a more mature and/or complete solution *right now* for managing your library, it doesn't get much better than that.\n\nHowever, there are several shortcomings that spawned the creation of Moe.\n\n* `No support for tags with multiple values <https://github.com/beetbox/beets/issues/505>`_.\n* `No native attachment/artifact support <https://github.com/beetbox/beets/pull/591>`_ i.e. the ability to move or query log files, album art, etc. with an album.\n* It's quite an intimidating codebase for new developers. Beets is a beast of a project, as when it was first conceived, Adrian didn't have access to all the fancy python libraries we have now. As a result, there is a *ton** of hand-written code and solutions that are arguably better dealt off to an external library e.g. database integration or cross-platform filesystem path handling. Because of it's immense size and complexity, it's fairly difficult for a developer to come in and try to understand everything that's going on. I think this is part of the reason beets has seen trouble gaining new maintainers or willing developers that want to help further it along its path. These days, Adrian has begun to focus on other projects, which means I don't believe we are likely to see any major changes to beets for the foreseeable future.\n* Most importantly, this is an area I'm passionate in, and felt it would be a valuable and fun learning experience creating my own app. I'm not a software developer by trade, so I greatly appreciate any feedback or thoughts anyone has as I go along.\n",
    'author': 'Jacob Pavlock',
    'author_email': 'jtpavlock@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MoeMusic/Moe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.7,<3.10',
}


setup(**setup_kwargs)
