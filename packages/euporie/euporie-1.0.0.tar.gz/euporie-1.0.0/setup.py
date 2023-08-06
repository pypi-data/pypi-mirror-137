# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['euporie',
 'euporie.app',
 'euporie.commands',
 'euporie.graphics',
 'euporie.key_binding',
 'euporie.key_binding.bindings',
 'euporie.markdown',
 'euporie.markdown.blocks',
 'euporie.menu',
 'euporie.output',
 'euporie.render',
 'euporie.render.image']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0,<10.0',
 'aenum>=3.1,<4.0',
 'appdirs>=1.4,<2.0',
 'flatlatex>=0.15,<0.16',
 'jsonschema>=4.4,<5.0',
 'jupyter-client>=7.1,<8.0',
 'nbformat>=5,<6',
 'prompt-toolkit>=3.0,<4.0',
 'pyperclip>=1.8,<2.0',
 'rich>=11,<12']

extras_require = \
{':extra == "all"': ['timg>=1.1,<2.0'],
 'all': ['mtable>=0.1,<0.2',
         'html5lib>=1.1,<2.0',
         'sympy>=1.9,<2.0',
         'antlr4-python3-runtime>=4.9,<5.0',
         'CairoSVG>=2.5,<3.0'],
 'html-mtable': ['mtable>=0.1,<0.2', 'html5lib>=1.1,<2.0'],
 'images-img2unicode': ['img2unicode>=0.1a8,<0.2'],
 'latex-sympy': ['sympy>=1.9,<2.0', 'antlr4-python3-runtime>=4.9,<5.0'],
 'svg-cairosvg': ['CairoSVG>=2.5,<3.0']}

entry_points = \
{'console_scripts': ['euporie = euporie.app:App.launch']}

setup_kwargs = {
    'name': 'euporie',
    'version': '1.0.0',
    'description': 'Euporie is a text-based user interface for running and editing Jupyter notebooks',
    'long_description': '#######\neuporie\n#######\n\n|PyPI| |RTD| |Binder| |License| |Stars|\n\n.. content_start\n\n**Euporie is a text-based user interface for running and editing Jupyter notebooks.**\n\nThe interface is similar to JupyterLab or Jupyter Notebook, and supports keyboard or mouse navigation.\n\nView the online documentation at: `https://euporie.readthedocs.io/ <https://euporie.readthedocs.io/>`_\n\n----\n\n.. image:: https://user-images.githubusercontent.com/12154190/151821363-9176faac-169f-4b12-a83f-8a4004e5b9bb.png\n   :target: https://user-images.githubusercontent.com/12154190/151821363-9176faac-169f-4b12-a83f-8a4004e5b9bb.png\n\n`View more screenshots here <https://euporie.readthedocs.io/en/latest/pages/gallery.html>`_\n\n*******\nInstall\n*******\n\nYou can install euporie with `pipx <pipxproject.github.io/>`_:\n\n.. code-block:: console\n\n   $ pipx install euporie\n\nYou can also try euporie online `here <https://mybinder.org/v2/gh/joouha/euporie-binder/HEAD?urlpath=%2Feuporie%2F>`_.\n\n********\nFeatures\n********\n\n* Edit and run notebooks in the terminal\n* Open multiple notebooks\n* Code completion\n* Suggests line completions from history\n* Hightly configurable\n* Print formatted notebooks to the terminal or pager\n* Displays rich cell outputs, including:\n\n   * Markdown\n   * Tables\n   * Images\n   * LaTeX\n   * HTML\n   * SVG\n\n*************\nCompatibility\n*************\n\nEuporie requires Python 3.8 or later. It works on Linux, Windows and MacOS\n\n\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/euporie.svg\n    :target: https://pypi.python.org/projects/euporie/\n    :alt: Latest Version\n\n.. |RTD| image:: https://readthedocs.org/projects/euporie/badge/\n    :target: https://euporie.readthedocs.io/en/latest/\n    :alt: Documentation\n\n.. |Binder| image:: https://mybinder.org/badge_logo.svg\n   :target: https://mybinder.org/v2/gh/joouha/euporie-binder/HEAD?urlpath=%2Feuporie%2F\n   :alt: Launch with Binder\n\n.. |License| image:: https://img.shields.io/github/license/joouha/euporie.svg\n    :target: https://github.com/joouha/euporie/blob/main/LICENSE\n    :alt: View license\n\n.. |Stars| image:: https://img.shields.io/github/stars/joouha/euporie\n    :target: https://github.com/joouha/euporie/stargazers\n    :alt: ⭐\n',
    'author': 'Josiah Outram Halstead',
    'author_email': 'josiah@halstead.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joouha/euporie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
