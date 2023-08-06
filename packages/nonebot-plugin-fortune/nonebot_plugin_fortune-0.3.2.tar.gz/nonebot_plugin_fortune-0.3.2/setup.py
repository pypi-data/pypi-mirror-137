# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_fortune']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'pillow>=9.0.0,<10.0.0',
 'ujson>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-fortune',
    'version': '0.3.2',
    'description': 'Fortune divination!',
    'long_description': '<div align="center">\n\n# Fortune\n\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable-next-line MD036 -->\n_🙏 今日运势 🙏_\n<!-- prettier-ignore-end -->\n\n</div>\n<p align="center">\n  \n  <a href="https://github.com/KafCoppelia/nonebot_plugin_fortune/blob/main/LICENSEE">\n    <img src="https://img.shields.io/badge/license-MIT-informational">\n  </a>\n  \n  <a href="https://github.com/nonebot/nonebot2">\n    <img src="https://img.shields.io/badge/nonebot2-2.0.0beta.1-green">\n  </a>\n  \n  <a href="">\n    <img src="https://img.shields.io/badge/release-v0.3.2-orange">\n  </a>\n  \n</p>\n\n</p>\n\n## 版本\n\nv0.3.2\n\n⚠ 适配nonebot2-2.0.0beta.1；适配alpha.16参见[alpha.16分支](https://github.com/KafCoppelia/nonebot_plugin_fortune/tree/alpha.16)\n\n## 安装\n\n1. 安装方式注意：\n\n    - 通过`pip`或`nb`：版本指定`^0.3.2`，pypi无法发行过大安装包，由此安装的插件不包含所有`resource`下所有主题抽签资源，需单独下载，建议`zip`包下载后单独提取`resource`资源，后更改`FORTUNE_PATH`配置即可；\n    \n    - 通过`zip`或`git clone`安装：包含`resource`下所有主题抽签资源；\n\n2. 抽签签底`img`、字体`font`、文案`fortune`等资源位于`./resource`下，可在`env`下设置`FORTUNE_PATH`更改；\n\n```python\nFORTUNE_PATH="your_path_to_resource"   # 默认位于os.path.join(os.path.dirname(__file__), "resource")，具体查看data_source.py\n```\n\n3. **新增** 更多抽签主题，在`env`下设置`xxx_FLAG`以启用或关闭抽签随机主题，例如：\n\n```python\nARKNIGHTS_FLAG = true         # 明日方舟\nASOUL_FLAG = true             # A-SOUL\nAZURE_FLAG = true             # 碧蓝航线\nGENSHIN_FLAG = true           # 原神\nONMYOJI_FLAG = true           # 阴阳师\nPCR_FLAG = true               # 公主链接\nTOUHOU_FLAG = true            # 东方\nTOUHOU_OLD_FLAG = true        # 东方旧版\nVTUBER_FLAG = true            # Vtuber\nPUNISHING_FLAG = true         # 战双帕弥什\nGRANBLUE_FANTASY_FLAG = true  # 碧蓝幻想\nPRETTY_DERBY_FLAG = true      # 赛马娘\n```\n\n4. **新增** 在`./resource/fortune_setting.json`内配置**指定抽签**规则，例如：\n\n```json\n{\n    "group_rule": {\n        "123456789": "random",\n        "987654321": "azure",\n        "123454321": "granblue_fantasy"\n    },\n    "specific_rule": {\n        "凯露": [\n            "pcr\\/frame_1.jpg",\n            "pcr\\/frame_2.jpg"\n        ],\n        "可可萝": [\n            "pcr\\/frame_41.jpg"\n        ]\n    }\n}\n```\n\n*group_rule会自动生成，specific_rule可手动配置*\n\n指定凯露签，由于存在两张凯露的签底，配置凯露签的**路径列表**即可，其余类似，**请确保图片格式输入正确**；目前仅能通过`json`配置规则；\n\n5. 占卜一下你的今日运势！🎉\n\n## 功能\n\n1. 随机抽取今日运势，配置**更多**种抽签主题：原神、PCR、Vtuber、东方、明日方舟、旧版东方、赛马娘、阴阳师、碧蓝航线、碧蓝幻想、战双帕弥什……\n\n2. 可配置随机抽签主题或指定主题，也可指定角色签底（例如可莉、魔理沙、凯露、**阿夸**🥰）；\n\n3. 每群每人一天限抽签1次，0点刷新（贪心的人是不会有好运的🤗）；\n\n4. 抽签的信息会保存在`./resource/fortune_data.json`内；群抽签设置及指定抽签规则保存在`./resource/fortune_setting.json`内；抽签生成的图片当天会保存在`./resource/out`下；\n\n## 命令\n\n1. 一般抽签：今日运势、抽签、运势；\n\n2. 指定签底并抽签：指定[xxx]签，在`./resource/fortune_setting.json`内手动配置；\n\n3. [群管或群主或超管] 配置抽签主题：\n\n    - 设置[原神/pcr/东方/vtb/xxx]签：设置群抽签主题；\n\n    - 重置抽签：设置群抽签主题为随机；\n\n4. 抽签设置：查看当前群抽签主题的配置；\n\n5. **新增** [超管] 刷新抽签：即刻刷新抽签，防止过0点未刷新的意外。\n\n## 效果\n\n测试效果出自群聊。\n\n![display](./display.jpg)\n\n## 本插件改自\n\n[opqqq-plugin](https://github.com/opq-osc/opqqq-plugin)\n\n## 抽签图片及文案资源\n\n1. [opqqq-plugin](https://github.com/opq-osc/opqqq-plugin)：原神、pcr、vtb抽签主题；\n\n2. 感谢江樂丝提供东方签底；\n\n3. [FloatTech-zbpdata/Fortune](https://github.com/FloatTech/zbpdata)：其余主题签；\n\n## 资源整合注意\n\n1. 抽签图片及文案资源下载参见上述出处链接，各抽签主题图片格式**未统一**；\n\n2. 本插件中未使用[FloatTech-zbpdata/Fortune](https://github.com/FloatTech/zbpdata)提供的全部主题签，其提供的`text.json`文案资源与[opqqq-plugin](https://github.com/opq-osc/opqqq-plugin)提供的文案资源`copywriting.json`与`goodLuck.json`略有不同，具体不同如下：\n\n\t- `text.json`中`title`（吉凶度设定）直接对应`content`（运势文案内容）；\n\n\t- 而`goodLuck.json`中`good-luck`（吉凶度编号）对应`name`（吉凶度设定）；`copywriting.json`中`good-luck`（吉凶度编号）对应`content`（运势文案内容）；\n',
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
