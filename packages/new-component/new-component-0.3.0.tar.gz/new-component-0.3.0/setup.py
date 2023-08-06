# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['new_component']

package_data = \
{'': ['*'], 'new_component': ['templates/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'colorama>=0.4.4,<0.5.0',
 'shellingham>=1.4.0,<2.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['new-component = new_component.__main__:main']}

setup_kwargs = {
    'name': 'new-component',
    'version': '0.3.0',
    'description': 'Quickly create opinionated Styled Components for React Projects',
    'long_description': '# new-component\n\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![ci](https://github.com/iancleary/new-component/workflows/ci/badge.svg)](https://github.com/iancleary/new-component/actions/workflows/ci.yml)\n\nIan Cleary ([iancleary](https://github.com/iancleary))\n\n## Description\n\n**Welcome!** This is a CLI for creating [styled-components](https://styled-components.com) for React projects quickly.\n\n> Note: I\'ve rewrote Josh W Comeau\'s [new-component](https://www.npmjs.com/package/new-component) NPM package in Python 🐍 and adapted it to my preferences. It is an excellent project and you should check it out!\n\nI didn\'t understand styled components at first. At the time of this writing, I\'m looking to develop my understanding of CSS, upon the advice of Josh W Comeau\'s blog post "[The styled-components Happy Path](https://www.joshwcomeau.com/css/styled-components/)".\n\nAfter you read that article, you\'ll gather that this CLI aims to combine the wisdom of Josh\'s templates with my personal preferences.\n\n- Adding the `import styled from "styled-components"` in the new `component.js` file.\n- Adding a `styled.Wrapper` component definition (and making it .the parent html element in the React Component\'s `render` function)\n\n## Quickstart\n\n```sh\n❯ pipx install new-component\n❯ new-component --help\n```\n\nThat will output the following:\n\n```\nUsage: new_component [OPTIONS] NAME\n\n  Creates an new component directory in a React project, with opinionated\n  defaults for styled-components.\n\n  See https://styled-components.com/ for more information.\n\nArguments:\n  NAME  Name of component to create.  [required]\n\nOptions:\n  -d, --directory TEXT  The directory in which to create the component.\n                        [default: src/components/]\n  -e, --extension TEXT  The file extension for the created component files.\n                        [default: js]\n  -v, --version         Show the application\'s version and exit.\n  --install-completion  Install completion for the current shell.\n  --show-completion     Show completion for the current shell, to copy it or\n                        customize the installation.\n  --help                Show this message and exit.\n```\n\n## Example Usage\n\nThe first and only argument is the name of the component to create.\n\n```bash\n❯ new-component Backdrop\nCreated a new Backdrop Component 💅 🚀!\n/Users/iancleary/Personal/new-component/src/components/Test4\n```\n\nThe path printed is the absolute path to new component folder.\n\n> It will very based upon your setup!\n\nThis command created two files:\n\n`src/components/Backdrop/index.js`\n`src/components/Backdrop/Backdrop.js`\n\nThe contents of the files will be as follows:\n\n```js\n// `src/components/Backdrop/index.js`\nexport { default } from "./Backdrop"\n```\n\n```js\n// `src/components/Backdrop/Backdrop.js`\nimport React from "react"\nimport styled from "styled-components"\n\nconst Backdrop = ({children}) => {\n  return (\n    <Wrapper>\n      {children}\n    </Wrapper>\n  )\n};\n\nconst Wrapper = styled.div`\n  /* CSS Goes Here */\n`\n\nexport default Backdrop\n```\n\n## Configuration\n\nConfiguration can be done through 3 different ways:\n\n* Creating a global `settings.json` in your home directory (`~/.config/new-component/settings.json`).\n* Creating a local `.new-component-config.json` in your project\'s root directory.\n* Command-line arguments.\n\nThe resulting values are merged, with command-line values overwriting local values, and local values overwriting global ones.\n\n## API Reference\n\n### Directory\n\nControls the desired directory for the created component. Defaults to src/components\n\nUsage:\n\nCommand line: `--directory <value>` or `-d <value>`\n\nJSON config: `{ "directory": <value> }`\n\n### File Extension\n\nControls the file extension for the created components. Can be either js (default) or jsx.\n\nUsage:\n\nCommand line: `--extension <value> or -e <value>`\n\nJSON config: `{ "extension": <value> }`\n\n## Further information\n\n> I will likely evolve this CLI as I learn more; I\'m on my way 😊\n\n- Add different component types\n- Promote better patterns to ensure CSS (single source of styles, Isolated CSS)\n\nThanks to Josh W Comeau\'s blog post "[The styled-components Happy Path\n](https://www.joshwcomeau.com/css/styled-components/) for starting my education! Again, it puts this README in perspective.\n\n**Enjoy quickly creating styled components 💅 🚀!**\n\n## Contributing\n\nI created this CLI for my opinionated uses and may not accept changes.\n\nSee [CONTRIBUTING.md](.github/CONTRIBUTING.md).\n',
    'author': 'Ian Cleary',
    'author_email': 'contact@iancleary.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iancleary/new-component',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
