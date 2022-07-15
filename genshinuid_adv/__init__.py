from ..all_import import * # noqa: F401, F403
from .get_adv import char_adv, weapon_adv

get_char_adv = on_regex('([\u4e00-\u9fa5]+)(用什么|能用啥|怎么养)', priority=priority)
get_weapon_adv = on_regex('([\u4e00-\u9fa5]+)(能给谁|给谁用|要给谁|谁能用)', priority=priority)

@get_char_adv.handle()
@handle_exception('建议')
async def send_char_adv(matcher: Matcher, args: Tuple[Any, ...] = RegexGroup()):
    im = await char_adv(args[0])
    await matcher.finish(im)


@get_weapon_adv.handle()
@handle_exception('建议')
async def send_weapon_adv(matcher: Matcher, args: Tuple[Any, ...] = RegexGroup()):
    im = await weapon_adv(args[0])
    await matcher.finish(im)