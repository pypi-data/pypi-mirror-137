# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot-plugin-txt2img']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot==2.0.0-beta.1',
 'nonebot2==2.0.0-beta.1',
 'pillow>=9.0.0,<10.0.0',
 'requests>=2.27.1,<3.0.0',
 'wcwidth>=0.2.5,<0.3.0']

setup_kwargs = {
    'name': 'nonebot-plugin-txt2img',
    'version': '0.1.0',
    'description': '轻量文字转图片插件',
    'long_description': '<!-- markdownlint-disable MD033 MD041-->\n<p align="center">\n  <img src="https://cdn.jsdelivr.net/gh/mobyw/images@main/Screenshots/nonebot-plugin-txt2img.png" width="400px"/>\n</p>\n\n<div align="center">\n\n# nonebot-plugin-txt2img\n\n_✨ 轻量文字转图片插件 ✨_\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/mobyw/nonebot-plugin-txt2img/master/LICENSE">\n    <img src="https://img.shields.io/github/license/mobyw/nonebot-plugin-txt2img.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-txt2img">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-txt2img.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">\n</p>\n\n## 简介\n\n**请注意：此插件仅适配 nonebot2 2.0.0b1 及以上。**\n\n本插件由使用 `PIL` 库将纯文字消息转为图片，启动时会检测所需资源是否存在，若不存在会自动下载到对应位置。生成的图片以 `base64` 格式发送，不保存到磁盘。\n\n## 安装步骤\n\n### 安装 NoneBot2\n\n完整文档可以在 [这里](https://v2.nonebot.dev/) 查看。\n\n请在创建项目时选用 `onebot v11` 适配器，并且按照文档完成最小实例的创建。\n\n### 安装 nonebot-plugin-txt2img\n\n使用 `pip` 安装：\n\n```bash\npip install nonebot-plugin-txt2img\n```\n\n在 `bot.py` 文件添加以下代码加载插件：\n\n```\nnonebot.load_plugin("nonebot-plugin-txt2img")\n```\n\n## 指令说明\n\n指令匹配方式添加了 `to_me()` 规则，在群聊中使用时需要在命令首部或尾部添加 `@{bot_self_id}` 或 `{bot_nickname}`。\n\n**使用指令**：txt2img\n\n发送指令后根据提示输入标题、内容与字体大小，即可完成图片生成。\n\n* 标题：以 `1.5` 倍字体大小排版在首行居中位置。\n* 内容：以 `1` 倍字体大小左对齐排版。\n* 字体大小：位于 `10~120` 之间的数字。\n\n## 项目致谢\n\n本项目基于以下项目或服务实现，排名不分先后。\n\n* [nonebot2](https://github.com/nonebot/nonebot2)\n* [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)\n* [txt2img](https://github.com/taseikyo/txt2img)\n',
    'author': 'mobyw',
    'author_email': 'mobyw66@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mobyw/nonebot-plugin-txt2img',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
