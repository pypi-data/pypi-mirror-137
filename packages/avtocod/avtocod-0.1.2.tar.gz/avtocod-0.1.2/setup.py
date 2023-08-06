# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avtocod',
 'avtocod.methods',
 'avtocod.session',
 'avtocod.types',
 'avtocod.types.profile',
 'avtocod.types.review']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'contextvars>=2.4,<3.0', 'pydantic>=1.8.2,<1.9.0']

setup_kwargs = {
    'name': 'avtocod',
    'version': '0.1.2',
    'description': 'Avtocod - неофициальный, элегантный, асинхронный враппер автокода',
    'long_description': '<p align="center">\n    <a href="https://github.com/Fom123/avtocod">\n        <img src="https://profi.avtocod.ru/img/icons/apple-touch-icon-152x152.png" alt="Pyrogram" width="128">\n    </a>\n    <br>\n    <b>Avtocod - неофициальная Python библиотека</b>\n    <br>\n</p>\n\n**Avtocod** - неофициальный, элегантный, асинхронный враппер [автокода](https://profi.avtocod.ru/).\nПозволяет взаимодействовать с апи автокода используя лишь данные от учетной записи.\n\n### Ключевые особенности\n- **Быстрый**\n- **Поддержка тайпхинтов**\n- **Асинхронный код**\n\n\n### Требования\n\n- Python 3.8 или выше.\n- [Аккаунт Автокода](https://profi.avtocod.ru/auth).\n\n\n### Установка\n\n``` bash\npip3 install -U avtocod\n```\n\n\n### Документация\n\nВременно, вместо документации, вы можете использовать [примеры](examples)\n\n\n### Внесение своего вклада в проект\n\nЛюбой вклад в проект приветствуется.\n\n### Благодарности\n\n- [@JrooTJunior](https://github.com/JrooTJunior) за [Aiogram](https://github.com/aiogram/aiogram). Выбрал вас в качестве примера\n',
    'author': 'Fom123',
    'author_email': 'gamemode1.459@gmail.com',
    'maintainer': 'Fom123',
    'maintainer_email': 'gamemode1.459@gmail.com',
    'url': 'https://github.com/Fom123/avtocod',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
