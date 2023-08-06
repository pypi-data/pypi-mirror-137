# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mg_file',
 'mg_file.file',
 'mg_file.file.test',
 'mg_file.sql_raw',
 'mg_file.sql_raw.async_sql',
 'mg_file.sql_raw.sync_sql',
 'mg_file.sql_raw.test',
 'mg_file.sqllite_orm',
 'mg_file.sqllite_orm.test']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'loguru>=0.6.0,<0.7.0', 'prettytable>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'mg-file',
    'version': '0.1.5',
    'description': 'Удобное пользование файлами',
    'long_description': '# Что это\n\nБиблиотека для работы с файлами и СУБД\n\n# Установка через [`pip`](https://pypi.org/project/mg-file/)\n\n```bash\npip install mg-file\n```\n\n# Технологии\n\n| Технологии                                      | Описание                                                      |\n|-------------------------------------------------|---------------------------------------------------------------|\n| [Файлы](mg_file/file/README.md)                 | Работа с `txt`, `csv` , `json` , `pickl`                      |\n| [Чистый SQL запросы](mg_file/sql_raw/README.md) | Синхронный / Асинхронный доступ к СУБД `PostgreSQL` , `MySql` |\n| [SQL ORM](mg_file/sqllite_orm/README.md)        | `ORM` система                                                 |\n\n\n',
    'author': 'Denis Vetkin',
    'author_email': 'denis-kustov@rambler.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/denisxab/mg_file',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
