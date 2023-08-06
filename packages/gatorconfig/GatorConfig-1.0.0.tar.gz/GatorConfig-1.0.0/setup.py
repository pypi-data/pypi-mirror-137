# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gatorconfig', 'gatorconfig.gui']

package_data = \
{'': ['*']}

install_requires = \
['gatoryaml>=1.0.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'ruamel.yaml>=0.17.20,<0.18.0',
 'typer>=0.4.0,<0.5.0']

extras_require = \
{'gui': ['PyQt6>=6.2.2,<7.0.0']}

entry_points = \
{'console_scripts': ['gatorconfig = gatorconfig.gator_config:cli']}

setup_kwargs = {
    'name': 'gatorconfig',
    'version': '1.0.0',
    'description': 'Autogeneration of GatorGradle configuration files.',
    'long_description': '# GatorConfig\n\n![logo](https://user-images.githubusercontent.com/42869122/152203388-39f5f0ef-e4c7-4f80-b667-07a4ed739b4d.png)\n\nA simple Python tool utilizing both a CLI and GUI approach\nto automate the generation of configuration files for\n[GatorGrader](https://github.com/GatorEducator/gatorgrader).\nThis tool is designed to assist educators in grading\nGitHub-based assignments for their computer science courses.\n\n## Requirements\n\n- [Python](https://realpython.com/installing-python/)\n- [Pipx](https://pypa.github.io/pipx/installation/)\n- [Poetry](https://python-poetry.org/docs/#installing-with-pipx)\n\n## Usage\n\n### Install with pip or pipx\n\nTo install the tool and its dependencies using pip, run the following command:\n\n```bash\npip install gatorconfig\n```\n\nAlternatively, you can install using pipx by running:\n\n```bash\npipx install gatorconfig\n```\n\n### Running GatorConfig\n\nGatorConfig is a tool that can utilize the command line interface, which\nwas built to accommodate the users. To run the GatorConfig program\nin CLI, type the command:\n\n`gatorconfig`\n\nOnce you run this command, the program will output:\n\n`Wrote file to: C:\\Users\\<YOUR PATH>\\config\\gatorgrader.yml`\n\nThis command will auto-generate a default configuration file for GatorGradle\nnamed `gatorgrader.yml` located in the `config` folder.\n\nAdditionally, you can run the `gatorconfig --help` for more\ninformation about the configuration. This command will list the variables\nin the file as well as the defaults it outputs.\n\n## Contributing\n\n### Technical details\n\nThe GitHub Actions\nworkflow executes [pytest](https://pytest.org/) (with\n[coverage](https://pypi.org/project/pytest-cov/)) and\n[pylint](https://pylint.org/) using the Poetry configuration, and checks\nmarkdown with [markdownlint](https://github.com/DavidAnson/markdownlint) and\nspelling with [cspell](https://cspell.org/).\n\n### Installing Python dependencies\n\nAfter cloning this project, you will likely want to instruct Poetry to create a\nvirtual environment and install the Python packages (such as pytest and pylint)\nlisted in `pyproject.toml`.\n\nTo install Python dependencies:\n\n```bash\npoetry install -E gui\n```\n\nTo install without the extra GUI feature, install with:\n\n```bash\npoetry install\n```\n\n### Running tasks\n\nThis project uses the [taskipy](https://github.com/illBeRoy/taskipy) task runner\nto simplify testing and linting. You can see the actual commands run when tasks\nare executed under the `[tool.taskipy.tasks]` header in `pyproject.toml`.\n\n- **Test** your code with `poetry run task test`\n- **Lint** your code with `poetry run task lint`\n\n## Authors\n\n- Wesley Long, @WesleyL30 - *Lead CLI developer*\n- Danny Ullrich, @ullrichd21 - *Lead GUI developer*\n- Kobe Coleman, @ColemanKobe\n- Paige Downey, @PaigeCD\n- Favour Ojo, @favourojo\n',
    'author': 'Daniel Ullrich',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cmpsc-481-s22-m1/GatorConfig',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
