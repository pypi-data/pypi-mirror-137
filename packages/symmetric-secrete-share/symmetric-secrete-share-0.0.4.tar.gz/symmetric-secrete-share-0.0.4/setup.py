# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sss_cli']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.5.0,<2.0.0', 'requests>=2.27.1,<3.0.0', 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['sss = sss_cli.__main__:app',
                     'symmetric-secrete-share = sss_cli.__main__:app',
                     'tts = sss_cli.__main__:app']}

setup_kwargs = {
    'name': 'symmetric-secrete-share',
    'version': '0.0.4',
    'description': 'Share secret files via github with symmetric encryption ed25519.',
    'long_description': '# symmetric-secrete-share\n\nShare secret files via github with symmetric encryption ed25519.\n\n- **IMPORTANT: The secret files at should be git-ignored.**\n- Temporarily supports only text files (only tested with `.env`).\n- Best used to store secrets and configurations.\n- Key should be a 32-byte long string.\n- (FAQ) If you share with GitHub, please notice that there\'s a 5 minutes cool-down on refreshing. [Details](https://stackoverflow.com/questions/46551413/github-not-update-raw-after-commit)\n\n## Use\n\n1. Install CLI\n2. Check the [Tutorial](#Tutorial) and `sss --help`\n3. Recommend to set a global key with `sss key`\n4. Get a config like `$REPO_ROOT/test/injection/sss.json`. The json-schema inside will help you write it.\n\n### inject\n\n1. Get a config file like `$REPO_ROOT/test/injection/sss.json`. The json-schema inside will help you write it.\n2. run CLI\n\n   ```bash\n   sss inject [-k TEXT] CONFIG_PATH\n   ```\n\n### share\n\n- **IMPORTANT: The generated secret (`*.encrypted`) at should be git-ignored to avoid oblivious leakage.**\n\n1. Run CLI\n\n   ```bash\n   sss share [-k TEXT] CONFIG_PATH\n   ```\n\n2. Upload the generated file to GitHub (or other platforms).\n3. Update the config file if needed.\n\n## Contribute\n\n- Created for [Artcoin-Network](https://github.com/Artcoin-Network/), modifying the private repo[Artcoin-Network/artificial-dev-config](https://github.com/Artcoin-Network/artificial-dev-config).\n- Read More in [dev-docs.md](./docs/dev-docs.md)\n\n## Tutorial\n\nIn this tutorial, all commands are assumed to run under the `$REPO_ROOT`. We are going to use these concepts:\n\n- key: `This key contains 32 characters.`.\n- URL: `https://raw.githubusercontent.com/PabloLION/symmetric-secrete-share/main/tests/example.encrypted`.\n- key chain: A file to share key, initialized with `sss key`.\n\nWe are going to play with the folder `test/injection`, with the `sss.json` file inside it. To share your own file, a new config file should be created.\n\n### Setup a local key chain\n\n```bash\nsss key # create/edit\nsss key -c # clear all keys\n```\n\n### load files from URL\n\nThese code will generate a `test/injection/target.env` like `test/example.env`\n\n```bash\nsss inject ./tests/injection/sss.json # use key from initial key chain\nsss inject -k "This key contains 32 characters." ./tests/injection/sss.json\nsss inject ./tests/injection/sss.json -k "I\'m a string with 32 characters." # fail\n```\n\n### share files\n\nNeed to upload manually #TODO\nThese code will generate a `test/injection/target.encrypted`\n\n```bash\nsss share ./tests/injection/sss.json # use key from initial key chain\nsss share -k "This key contains 32 characters." ./tests/injection/sss.json\n```\n',
    'author': 'Pablion',
    'author_email': '36828324+Pablion@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
