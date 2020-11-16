from nonebot import on_command, CommandSession
import requests
from .RSSHub import rsshub
from .RSSHub import RSS_class
from .RSSHub import RWlist
from .RSSHub import rsstrigger as TR
import logging
from nonebot.log import logger
from nonebot.permission import *
import hoshino
import nonebot


# on_command 装饰器将函数声明为一个命令处理器
@on_command('show_all', aliases=('showall','seeall'), permission=GROUP_ADMIN|SUPERUSER)
async def show_all(session: CommandSession):
    #rss_name = session.get('show_all', prompt='查看所有订阅')
    
    user_id = session.ctx['user_id']
    try:
        group_id = session.ctx['group_id']
    except:
        group_id = None
    #print(type(user_id),type(config.ROOTUSER))
    flag = 0
    msg = ''
    try:
        list_rss = RWlist.readRss()
    except:
        await session.send('获取rss列表失败')
        return
    if group_id:
        try:
            for rss_ in list_rss:
                if str(group_id) in str(rss_.group_id):
                    msg = msg + '名称：' + rss_.name + '\n订阅地址：' + rss_.url + '\n\n'
                    flag += 1
                    if(flag%5==0):
                        await session.send(msg)
                        msg = ''
            if flag <= 0:
                await session.send('没有找到订阅哟！')
            else:
                await session.send(msg + '共' + str(flag) + '条订阅')
        except:
            await session.send('本群还没有任何订阅！')
    elif user_id:
        # 获取、处理信息
        try:
            for rss_ in list_rss:
                msg = msg + '名称：' + rss_.name + '\n订阅地址：' + rss_.url + '\n\n'
                flag += 1
                #每条信息展示 5 条订阅
                if(flag%5==0):
                    await session.send(msg)
                    msg = ''
            if flag <= 0:
                await session.send('没有找到订阅哟！')
            else:
                await session.send(msg + '共' + str(flag) + '条订阅')
        except:
            await session.send('还没有任何订阅！')
    else:
        await session.send('你没有权限进行此操作！')


# add.args_parser 装饰器将函数声明为 add 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@show_all.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            session.state['show_all'] = stripped_arg
        return
