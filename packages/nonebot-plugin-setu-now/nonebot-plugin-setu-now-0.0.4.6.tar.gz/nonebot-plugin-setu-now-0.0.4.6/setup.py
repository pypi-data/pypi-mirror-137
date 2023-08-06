# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_setu_now']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.0,<1.0.0',
 'nonebot-adapter-onebot==2.0.0-beta.1',
 'nonebot2==2.0.0-beta.1',
 'webdav4>=0.9.3,<0.10.0']

setup_kwargs = {
    'name': 'nonebot-plugin-setu-now',
    'version': '0.0.4.6',
    'description': '另一个色图插件',
    'long_description': '# nonebot-plugin-setu-now\n\n- 另一个色图插件\n- 根据别人的改了亿点点\n- 现在可以色图保存到 `WebDAV` 服务器中来节省服务器空间(可选)\n- 采用**即时下载**并保存的方式来扩充*自己*色图库(可选)\n- 支持私聊获取~~特殊~~色图\n- 对临时聊天不生效, \n\n# 安装配置\n```\npip install -U nonebot-plugin-setu-now\n```\n\n## .env 默认配置 (不写应该也可以正常工作)\n\n```ini\nsetu_cd=60\nsetu_save=\nsetu_path=\nsetu_porxy=\nsetu_reverse_proxy=\nsetu_dav_url=\nsetu_dav_username=\nsetu_dav_password=\n```\n\n- `setu_cd` CD(单位秒) 可选 默认`60`秒\n- `setu_save` 保存模式 可选 `webdav`(保存到webdav服务器中) 或 `local`(本地) 或 留空,不保存\n- `setu_path` 保存路径 可选 当选择保存模式时可按需填写, 可不填使用默认\n  - webdav 可选 默认`/setu` `/setur18`  \n  - 本地 可选 默认`./data/setu` `./data/setur18`\n- `setu_porxy` 代理地址 可选 当pixiv反向代理不能使用时可自定义\n- `setu_reverse_proxy` pixiv反向代理 可选 默认 `i.pixiv.re` \n- webdav 设置 当选择保存保存模式为 `webdav` 时必须填写 \n  - `setu_dav_username` 用户名\n  - `setu_dav_password` 密码\n  - `setu_dav_url` webdav服务器地址\n\n~~所有配置都可选了,还能出问题吗?~~\n\n## bot.py\n\n```\nnonebot.load_plugin("nonebot_plugin_setu_now")\n```\n\n# 使用\n\n- 指令 `(setu|色图|涩图|来点色色|色色|涩涩)\\s?(r18)?\\s?(.*)?`\n  - 看不懂？\n    - `setu|色图|涩图|来点色色|色色|涩涩` 任意关键词\n    - `r18` 可选 仅在私聊可用 群聊直接忽视\n    - `关键词` 可选\n- 例子\n  - `来点色色 妹妹`\n  - `setur18`\n',
    'author': 'kexue',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kexue-z/nonebot-plugin-setu-now',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
