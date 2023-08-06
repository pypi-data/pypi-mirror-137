# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_tmp',
 'fast_tmp.admin',
 'fast_tmp.admin.schema',
 'fast_tmp.admin.schema.forms',
 'fast_tmp.conf',
 'fast_tmp.jinja_extension',
 'fast_tmp.models',
 'fast_tmp.site',
 'fast_tmp.utils',
 'fastapi_cli',
 'fastapi_cli.tpl.app.{{cookiecutter.app_name}}',
 'fastapi_cli.tpl.app.{{cookiecutter.app_name}}.routes',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.tests',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}.apps',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}.apps.api',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}.apps.api.v1',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}.apps.api.v1.endpoints',
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}.{{cookiecutter.project_slug}}.enums']

package_data = \
{'': ['*'],
 'fast_tmp.admin': ['static/amis/*',
                    'static/css/*',
                    'static/img/*',
                    'static/js/*',
                    'templates/*'],
 'fastapi_cli': ['tpl/app/*',
                 'tpl/project/*',
                 'tpl/static/*',
                 'tpl/static/static/*'],
 'fastapi_cli.tpl.project.{{cookiecutter.project_slug}}': ['templates/*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['fast-tmp = fastapi_cli:main']}

setup_kwargs = {
    'name': 'fast-tmp',
    'version': '0.9.0',
    'description': '',
    'long_description': None,
    'author': 'Chise1',
    'author_email': 'chise123@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Chise1/fast-tmp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
