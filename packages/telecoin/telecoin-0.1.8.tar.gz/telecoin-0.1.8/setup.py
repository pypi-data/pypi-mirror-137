# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telecoin']

package_data = \
{'': ['*']}

install_requires = \
['Pyrogram==1.2.9', 'aiohttp==3.7.4.post0']

setup_kwargs = {
    'name': 'telecoin',
    'version': '0.1.8',
    'description': 'Simple library to make payments via telegram bitcoin exchangers',
    'long_description': "[![Downloads](https://pepy.tech/badge/telecoin)](https://pepy.tech/project/telecoin)\n[![Downloads](https://pepy.tech/badge/telecoin/month)](https://pepy.tech/project/telecoin)\n[![Downloads](https://pepy.tech/badge/telecoin/week)](https://pepy.tech/project/telecoin)\n![Score](https://www.code-inspector.com/project/29472/score/svg)\n![Score](https://www.code-inspector.com/project/29472/status/svg)\n### 💾 Installation\n\n```bash\npip install telecoin\n```\n\n---\n\n## 📞 Contacts\n* 🖱️ __Developer contacts: [![Dev-Telegram](https://img.shields.io/badge/Telegram-blue.svg?style=flat-square&logo=telegram)](https://t.me/marple_tech)__\n\n---\n\n## 🐦 Dependencies  \n\n| Library | Description                                            |\n|:-------:|:----------------------------------------------:        |\n|aiohttp  | Asynchronous HTTP Client/Server for asyncio and Python.|\n|pyrogram | Modern Telegram Framework                             |\n\n---\n\n\n## ❔ What is this? \n* This is simple library to activate @BTC_CHANGE_BOT, @Chatex_bot, @GetWallet_bot gift cheque. \n\n\n---\n\n## ↗️ Create Session\n```python\nimport asyncio\n\nfrom telecoin import BankerWrapper\n\n\nasync def main():\n    banker = BankerWrapper(phone_number='Your Number', api_id='Your ID',\n                           api_hash='Your Hash',\n                           session_name='i_love_telecoin')\n    await banker.create_session()\n\n\nif __name__ == '__main__':\n    asyncio.run(main())\n```\n\n---\n\n## 💰 Activate Cheque\n```python\nimport asyncio\n\nimport telecoin.exceptions\nfrom telecoin import BankerWrapper\n\n\nasync def main():\n    banker = BankerWrapper(phone_number='Your Number', api_id='Your ID',\n                           api_hash='Your Hash',\n                           session_name='i_love_telecoin')\n    try:\n        result = await banker.activate_cheque('https://telegram.me/BTC_CHANGE_BOT?start=c_ae0f629a49fd1b494b371c0ec64d1v21')\n        print(f'Received {result.btc} BTC / {result.rub} RUB')\n    except InvalidCheque:\n        print('Cheque is not valid')\n\n\nif __name__ == '__main__':\n    asyncio.run(main())\n\n```\n\n---\n\n",
    'author': 'Marple',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marple-git/telecoin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
