#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hoshino.typing import CQEvent, MessageSegment

from .. import chara
from hoshino import Service

ROSTER_HELP = '''花名册角色昵称补全计划
花名册 帮助 / roster help
花名册 列表 角色昵称 / roster list arg1
花名册 添加昵称 角色昵称 新增的角色昵称 / roster add arg1 arg2  
花名册 删除 角色昵称 删除的角色昵称 / roster remove arg1 arg2
花名册 设置默认昵称 角色昵称 默认的角色昵称 / roster default arg1 arg2
(角色昵称参数可以识别角色下所有昵称，建议先使用"谁是xx"来识别角色昵称，或者"花名册 列表 角色昵称"来识别角色所有昵称)
'''
sv = Service('pcr-roster', help_=ROSTER_HELP, bundle='pcr查询')


# 修改花名册功能 让万能的群友修改角色昵称
@sv.on_prefix('花名册')
async def roster_cmd(bot, ev: CQEvent):
    # sv.logger.info('花名册功能')
    # msg = ''
    # group_id = ev.group_id
    args = ev.message.extract_plain_text().split()
    # sv.logger.info(args)
    # sv.logger.info(len(args))
    if len(args) == 0:
        msg = ROSTER_HELP
        await bot.send(ev, msg)
    elif args[0] == '帮助' or args[0] == 'help':
        msg = ROSTER_HELP
        await bot.send(ev, msg)
    elif args[0] == '添加' or args[0] == 'add':
        if len(args) != 3:
            msg = f'参数格式错误，请重新输入或查询帮助...'
            await bot.send(ev, msg, at_sender=True)
            return
        # 需要修改的角色
        origin_name = args[1]
        nick_name = args[2]
        id_ = chara.name2id(origin_name)
        if id_ == chara.UNKNOWN:
            msg = f'兰德索尔似乎没有叫"{origin_name}"的人...'
            await bot.send(ev, msg)
        else:
            chara_name = chara.fromid(id_).name
            result = chara.add_nickname(id_, nick_name)
            if result:
                msg = f'角色"{chara_name}"添加昵称"{nick_name}"成功...'
            else:
                msg=f'角色"{chara_name}"已存在昵称"{nick_name}"...'
            await bot.send(ev, msg, at_sender=True)
            pass
    elif args[0] == '删除' or args[0] == 'remove':
        if len(args) != 3:
            msg = f'参数格式错误，请重新输入或查询帮助...'
            await bot.send(ev, msg, at_sender=True)
            return
        origin_name = args[1]
        nick_name = args[2]
        id_ = chara.name2id(origin_name)
        if id_ == chara.UNKNOWN:
            msg = f'兰德索尔似乎没有叫"{origin_name}"的人...'
            await bot.send(ev, msg)
        else:
            chara_name = chara.fromid(id_).name
            nicknames = chara.get_nicknames(id_)
            nicknames_len = len(nicknames)
            if nicknames_len == 1:
                msg = f'"{chara_name}"现在只有一个昵称了，需要至少保留一个...'
                await bot.send(ev, msg, at_sender=True)
                return
            remove_name = chara.remove_nickname(id_, nick_name)
            if remove_name:
                msg = f'成功删除"{chara_name}"的昵称"{remove_name}"...'
                await bot.send(ev, msg, at_sender=True)
            else:
                msg = f'角色"{chara_name}"不存在昵称"{remove_name}"...'
                await bot.send(ev, msg, at_sender=True)
    elif args[0] == '列表' or args[0] == 'list':
        if len(args) != 2:
            msg = f'参数格式错误，请重新输入或查询帮助...'
            await bot.send(ev, msg, at_sender=True)
            return
        origin_name = args[1]
        id_ = chara.name2id(origin_name)
        if id_ == chara.UNKNOWN:
            msg = f'兰德索尔似乎没有叫"{origin_name}"的人...'
            await bot.send(ev, msg)
        else:
            chara_name = chara.fromid(id_).name
            msg = f'"{chara_name}"的昵称列表为:\n'
            msg += f'索引\t昵称\n'
            nicknames = chara.get_nicknames(id_)
            for index, name in enumerate(nicknames):
                if index == len(nicknames):
                    msg += f'{index}\t{name}'
                else:
                    msg += f'{index}\t{name}'
            await bot.send(ev, msg, at_sender=True)
    elif args[0] == '设置默认名称' or args[0] == '设置默认昵称' or args[0] == 'default':
        if len(args) != 3:
            msg = f'参数格式错误，请重新输入或查询帮助...'
            await bot.send(ev, msg, at_sender=True)
            return
        origin_name = args[1]
        nick_name = args[2]
        id_ = chara.name2id(origin_name)
        if id_ == chara.UNKNOWN:
            msg = f'兰德索尔似乎没有叫"{origin_name}"的人...'
            await bot.send(ev, msg)
        else:
            chara_name = chara.fromid(id_).name
            reuslt = chara.default_nickname(id_, nick_name)
            if reuslt:
                msg = f'设置角色"{chara_name}"默认昵称"{nick_name}"成功...'
                await bot.send(ev, msg, at_sender=True)
            else:
                msg = f'角色"{chara_name}"不存在昵称"{nick_name}"...'
                await bot.send(ev, msg, at_sender=True)
