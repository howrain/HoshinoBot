from .RSSHub import rsstrigger as RT
from .RSSHub import del_cache as DC
from .RSSHub import rsshub
from .RSSHub import RSS_class
from .RSSHub import RWlist
import asyncio
import nonebot
import hoshino
async def start():
    bot = nonebot.get_bot()
    try:
        DC.delcache_trigger()
    except:
        print()

    try:
        rss_list = RWlist.readRss()  # 读取list
        for rss in rss_list:
            RT.rss_trigger(rss.time, rss)  # 创建检查更新任务
        #await bot.send_msg(message_type='private', user_id=hoshino.config.ROOTUSER[0], message='ELF_RSS 订阅器启动成功！')
    except Exception as e:
        #await bot.send_msg(message_type='private', user_id=hoshino.config.ROOTUSER[0], message='第一次启动，你还没有订阅，记得添加哟！')
        print(e)

loop = asyncio.get_event_loop()
loop.run_until_complete(start())
