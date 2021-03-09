
import hoshino
from hoshino import Service
from hoshino.typing import NoticeSession

sv1 = Service('退群通知', help_='退群通知')
@sv1.on_notice('group_decrease')
async def decrease_leave(session: NoticeSession):
    uid = session.event['user_id']
    bot = hoshino.get_bot()
    member=await bot.get_stranger_info(user_id=uid)
    nickname=member['nickname']
    msg = f'{nickname}({uid})退群了，期待再度相逢的那一天！'
    await session.send(msg)

sv2 = Service('入群欢迎', help_='入群欢迎')

@sv2.on_notice('group_increase')
async def increase_welcome(session: NoticeSession):
    
    if session.event.user_id == session.event.self_id:
        return  # ignore myself
    
    welcomes = hoshino.config.groupmaster.increase_welcome
    gid = session.event.group_id
    if gid in welcomes:
        await session.send(welcomes[gid], at_sender=True)
    # elif 'default' in welcomes:
    #     await session.send(welcomes['default'], at_sender=True)
