from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.plugin import on_command, on_message
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.exception import ActionFailed
from nonebot.adapters import Bot
from nonebot.typing import T_State
from ._role_info import avatar_info
#from ._function_doc import *
from asyncio import sleep
import random

guess_avartwo = on_command("从者推理", priority=1)
on_game = on_message()
finishGameSuddenly = on_command("终止从者推理",aliases={"结束从者推理","中止从者推理"},priority=1)

group_state = {

}  # 群游戏状态
group_exits = {

}  # 群上一次抽到的角色


async def del_msg(bot, message_id):
    try:
        await bot.delete_msg(message_id=message_id)
    except ActionFailed:
        pass


@guess_avartwo.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    gid = event.group_id
    if str(gid) not in group_state:
        group_state[str(gid)] = {
            "start": False,
            "roomMaster": str(event.user_id),
            "avar_num": "",
            "avar_info": {},
            "winner": [],
            "winner_name": []
        }
    try:
        if group_state[str(gid)]["start"] is True:
            await guess_avartwo.send("本局已经开始了一局游戏了哦")
        else:
            group_state[str(gid)]["start"] = True
            ava_num = random.randint(1, 245)  # 从者数据的初编号到末编号
            while str(gid) in group_exits and str(ava_num) == group_state[str(gid)]:
                avar_num = str(random.randint(1, 245))
            else:
                avar_num = str(ava_num)
            group_state[str(gid)]["avar_num"] = avar_num
            group_state[str(gid)]["avar_info"] = avatar_info[str(avar_num)]
            first_tips = group_state[str(gid)]["avar_info"]["height"]
            await guess_avartwo.send("第一条提示是，ta的身高：" + first_tips)
            await sleep(5)
            second_tips = group_state[str(gid)]["avar_info"]["weight"]
            await guess_avartwo.send("第二条提示是，ta的体重：" + second_tips)
            await sleep(5)
            third_tips = group_state[str(gid)]["avar_info"]["stair"]
            await guess_avartwo.send("第三条提示是，ta的职介：" + third_tips)
            await sleep(5)
            fourth_tips = group_state[str(gid)]["avar_info"]["like"]
            await guess_avartwo.send("第四条提示是，ta喜欢的东西：" + fourth_tips)
            await sleep(5)
            fifth_tips = group_state[str(gid)]["avar_info"]["dislike"]
            await guess_avartwo.send("最后一条提示是，ta讨厌的东西：" + fifth_tips + "\n游戏将在十秒内结束！")
            await sleep(10)
            if len(group_state[str(gid)]["winner"]) == 0:
                result = "本局没有人答对哦！"
                answer = group_state[str(gid)]["avar_info"]
                other_name = str(answer['other_name']) \
                    .replace('[', '') \
                    .replace(']', '') \
                    .replace(',', '，') \
                    .replace('\'', '')

                await guess_avartwo.send(f"游戏结束啦！本次游戏答案为{answer['name']}，\n"
                                         f"ta的别名有{other_name}" + result)
                del group_state[str(gid)]
                group_exits[str(gid)] = avar_num
            else:
                at = MessageSegment.at(int(group_state[str(gid)]["winner"][0]))
                result = "第一个答对的是"

                for i in group_state[str(gid)]["winner"]:
                    get_name = await bot.get_group_member_info(group_id=gid, user_id=int(i))
                    group_state[str(gid)]["winner_name"].append(get_name["nickname"])
                """for win in group_state[str(gid)]["winner"]:
                    if win == group_state[str(gid)]["winner"]:
                        write_doc_add("猜从者2", int(win), 2)  #该Function为数据库数据修改，如无需求请自行修改，下面同理
                    else:
                        write_doc_add("猜从者2", int(win), 1)"""
                answer = group_state[str(gid)]["avar_info"]
                other_name = str(answer['other_name']) \
                    .replace('[', ' ') \
                    .replace(']', ' ') \
                    .replace(',', '，') \
                    .replace('\'', ' ')
                await guess_avartwo.send(f"游戏结束啦！本次游戏答案为{answer['name']}，\n"
                                         f"ta的别名有{other_name}\n"
                                         f"{result}" + at
                                         + "\n所有答对的群员有：" +
                                         str(group_state[str(gid)]["winner_name"])
                                         .replace(',', '，')
                                         .strip('[').strip(']')
                                         .replace("\'", ""))
                del group_state[str(gid)]
    except Exception as e:
        if "KeyError" in repr(e):
            await guess_avartwo.send("游戏已被异常终止（可能为人为中止or出现了bug）请重新开始游戏！")
        else:
            raise


@on_game.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    gid = event.group_id
    uid = event.user_id
    message_id = event.message_id
    msg = str(event.message).strip()
    if str(gid) in group_state.keys():
        if msg == group_state[str(gid)]["avar_info"]["name"] or msg in \
                group_state[str(gid)]["avar_info"]["other_name"]:
            if str(uid) in group_state[str(gid)]["winner"]:
                await del_msg(bot, message_id)
                await on_game.send("你已经答对过了nano！留机会给别人吧", at_sender=True)
            else:
                await del_msg(bot, message_id)
                await on_game.send(MessageSegment.at(event.user_id) + "恭喜答对啦！")
                group_state[str(gid)]["winner"].append(str(uid))


@finishGameSuddenly.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    uid = event.user_id
    gid = event.group_id
    if str(gid) not in group_state:
        await finishGameSuddenly.send("本群目前无正在进行的游戏！")
    elif str(uid) != group_state[str(gid)]["roomMaster"]:
        at = MessageSegment.at(int(group_state[str(gid)]["roomMaster"]))
        await finishGameSuddenly.send("您不是房主！无法终止该局游戏!本局房主是"+at)
    else:
        del group_state[str(gid)]
        await finishGameSuddenly.send("游戏已终止，本局游戏胜败不计，如需重新开始游戏请发送【从者推理】")
