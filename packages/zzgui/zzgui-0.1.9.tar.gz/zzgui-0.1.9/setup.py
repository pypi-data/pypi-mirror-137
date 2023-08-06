# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zzgui', 'zzgui.qt5', 'zzgui.qt5.widgets']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.6,<6.0.0', 'QScintilla>=2.13.1,<3.0.0']

setup_kwargs = {
    'name': 'zzgui',
    'version': '0.1.9',
    'description': 'Python GUI toolkit',
    'long_description': '# The light Python GUI builder (currently based on PyQt5)\n\n# How to start \n## With docker && x11:\n```bash\ngit clone https://github.com/AndreiPuchko/zzgui.git\n#                      sudo if necessary \ncd zzgui/docker-x11 && ./build_and_run_menu.sh\n```\n## With PyPI package:\n```bash\npoetry new project_01 && cd project_01 && poetry shell\npoetry add zzgui\ncd project_01\npython -m zzgui > example_app.py && python example_app.py\n```\n## Explore sources:\n```bash\ngit clone https://github.com/AndreiPuchko/zzgui.git\ncd zzgui\npip3 install poetry\npoetry shell\npoetry install\npython3 demo/demo_01.py     # basic: main menu, form & widgets\npython3 demo/demo_02.py     # forms and forms in form\npython3 demo/demo_03.py     # grid form (CSV data), automatic creation of forms based on data\npython3 demo/demo_04.py     # progressbar, data loading, sorting and filtering\npython3 demo/demo_05.py     # nonmodal form\npython3 demo/demo_06.py     # code editor\npython3 demo/demo_07.py     # database app (4 tables, mock data loading) - requires a zzdb package\npython3 demo/demo_08.py     # database app, requires a zzdb package, autoschema\n```\n\n## demo/demo_03.py screenshot\n![Alt text](https://andreipuchko.github.io/zzgui/screenshot.png)\n# Build standalone executable \n(The resulting executable file will appear in the folder  dist/)\n## One file\n```bash\npyinstaller -F demo/demo.py\n```\n\n## One directory\n```bash\npyinstaller -D demo/demo.py\n```\n',
    'author': 'Andrei Puchko',
    'author_email': 'andrei.puchko@gmx.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
