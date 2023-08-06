# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_antiflash']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0', 'nonebot2>=2.0.0-beta.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-antiflash',
    'version': '0.1.0',
    'description': 'Anti flash pictures in groups',
    'long_description': '<div align="center">\n\n# Anti Flash\n\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable-next-line MD036 -->\n_🎇 反闪照 🎇_\n<!-- prettier-ignore-end -->\n\n</div>\n<p align="center">\n  \n  <a href="https://github.com/KafCoppelia/nonebot_plugin_antiflash/blob/main/LICENSEE">\n    <img src="https://img.shields.io/badge/license-MIT-informational">\n  </a>\n  \n  <a href="https://github.com/nonebot/nonebot2">\n    <img src="https://img.shields.io/badge/nonebot2-2.0.0beta.1-green">\n  </a>\n  \n  <a href="">\n    <img src="https://img.shields.io/badge/release-v0.2.0-orange">\n  </a>\n  \n</p>\n\n</p>\n\n## 版本\n\nv0.2.0\n\n⚠ 适配nonebot2-2.0.0beta.1；适配alpha.16版本参见[alpha.16分支](https://github.com/KafCoppelia/nonebot_plugin_antiflash/tree/alpha.16)\n\n## 安装\n\n1. 通过`pip`或`nb`安装，版本请指定`^0.2.0`；\n\n2. 在`env`内设置：\n\n```python\nANTI_FLASH_ON=true                          # 开启或关闭\nANTI_FLASH_GROUP=["123456789", "987654321"] # 指定群聊\n```\n\n## 功能\n\n⚠ **谨慎开启此项功能, 谨慎指定群聊**\n\n由于该功能过于危险，需指定特定群聊启用反闪照功能。\n\n## 本插件改自\n\n忘记出处了，找到了马上补上。',
    'author': 'KafCoppelia',
    'author_email': 'k740677208@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
