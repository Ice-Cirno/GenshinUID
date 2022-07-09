from pathlib import Path

from nonebot import Bot, get_bot, get_driver, on_command, on_regex, require
from nonebot.adapters.onebot.v11 import (ActionFailed, GroupMessageEvent, Message, MessageEvent, MessageSegment,
                                         PRIVATE_FRIEND, PrivateMessageEvent)
from nonebot.exception import FinishedException
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Depends, RegexGroup
from nonebot.permission import SUPERUSER

get_guide_pic = on_regex('([\u4e00-\u9fa5]+)(推荐|攻略)', priority=priority)
get_bluekun_pic = on_command('参考面板', priority=priority)
get_char_adv = on_regex('([\u4e00-\u9fa5]+)(用什么|能用啥|怎么养)', priority=priority)
get_weapon_adv = on_regex('([\u4e00-\u9fa5]+)(能给谁|给谁用|要给谁|谁能用)',
                          priority=priority)

@get_guide_pic.handle()
@handle_exception('建议')
async def send_guide_pic(matcher: Matcher, args: Tuple[Any, ...] = RegexGroup()):
    message = args[0].strip().replace(' ', '')
    with open(os.path.join(INDEX_PATH, 'char_alias.json'),
              'r',
              encoding='utf8') as fp:
        char_data = json.load(fp)
    name = message
    for i in char_data:
        if message in i:
            name = i
        else:
            for k in char_data[i]:
                if message in k:
                    name = i
    # name = str(event.get_message()).strip().replace(' ', '')[:-2]
    url = 'https://img.genshin.minigg.cn/guide/{}.jpg'.format(name)
    if httpx.head(url).status_code == 200:
        await matcher.finish(MessageSegment.image(url))
    else:
        return