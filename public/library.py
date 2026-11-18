from config import *

# ======以下是发信息模块分为机器人发 和监控群改

async def isPrivileges(chatId):
    # 权限判断
    try:
        groupType = await app.get_chat(chatId)
        member = await app.get_chat_member(chatId, "me")
        if member.privileges:
            privi = member.privileges
            if groupType.type.name == 'CHANNEL':
                if privi.can_delete_messages and privi.can_post_messages and privi.can_edit_messages and privi.can_invite_users:
                    return 0,groupType
            else:
                if privi.can_delete_messages and privi.can_invite_users:
                    return 0,groupType
        return 1,groupType
    except (FloodWait,BadRequest,ChannelPrivate) as e:
        return 2, {}
async def timeJob(arr):
    await app.delete_messages(arr.get('id'), message_ids=arr.get('message_ids'))
async def msgNotify(id=None,text='无',times=2):
    msgId = await app.send_message(chat_id=id,text=f"{str(text)} \n({times}秒后删除)",disable_web_page_preview=True)
    scheduler.add_job(timeJob, trigger='date',run_date=datetime.datetime.now() + datetime.timedelta(seconds=times),
                      args=({'id': msgId.chat.id,'message_ids':msgId.id},))
async def trafficStatistics():
    # 定时统计当天的数
    fleet_group_info_list = db.select(f"SELECT * FROM fleet_group_info")
    for fleet_group_info in fleet_group_info_list:
        try:
            link_invite = await app.edit_chat_invite_link(fleet_group_info[1], fleet_group_info[2])
            if link_invite and link_invite.is_revoked == False:
                db.update("UPDATE fleet_group_info SET invite_link=%s,input=%s WHERE id=%s",
                          (link_invite.invite_link, link_invite.member_count or 0, fleet_group_info[0]))
                print(fleet_group_info[1],link_invite.member_count or 0)
        except RPCError as e:
            print('编辑链接失败', e)
    group_list = db.select(f"SELECT * FROM group_list WHERE  state=2")
    if group_list:
        for group in group_list:
            ContS = db.select(f"SELECT (SELECT SUM(input) FROM fleet_group_info WHERE group_id={group[1]}) AS out_count, "
                              f"(SELECT SUM(input) FROM fleet_group_info WHERE link_group ={group[1]}) AS input_count")
            print(ContS)
            db.update("UPDATE group_list SET out_fan=%s,input_fan=%s WHERE id=%s",
                                   (ContS[0][0], ContS[0][1], group[0]))

# 检测其他机器人
async def examineOpponent(chatId):
    try:
        member = await app.get_chat_member(chatId, "hutui1bot")
        if member.status.name == "ADMINISTRATOR":
            return True
    except RPCError as e:
        return False
async def requestFleetGroupInfo(group_id,link_group):
    # 读取关联邀请url 不存在即创建
    while True:
        fleet_group_info = db.select(f"SELECT * FROM fleet_group_info WHERE group_id=%s AND link_group=%s ",(group_id, link_group))
        if fleet_group_info:
            return fleet_group_info[0][2]
            # try:
            #     link_invite = await app.edit_chat_invite_link(fleet_group_info[0][1],fleet_group_info[0][2])
            #     if link_invite and link_invite.is_revoked==False:
            #         db.update("UPDATE fleet_group_info SET invite_link=%s,input=%s WHERE id=%s",
            #                   (link_invite.invite_link,link_invite.member_count or 0,fleet_group_info[0][0]))
            #         return link_invite.invite_link
            #     else:
            #         db.delete("DELETE FROM fleet_group_info WHERE id=%s", (fleet_group_info[0][0],))
            #         print('删除了链接')
            # except RPCError as e:
            #     print('编辑链接失败',e)
            #     db.delete("DELETE FROM fleet_group_info WHERE id=%s", (fleet_group_info[0][0],))
        else:
            try:
                # print('生成新链接')
                link = await app.create_chat_invite_link(group_id)
                db.insert("INSERT INTO fleet_group_info (group_id,invite_link,link_group) VALUES(%s,%s,%s)",
                          (group_id, link.invite_link, link_group))
            except RPCError as e:
                # print('生成链接失败可能无权限',e)
                return False
async def marshalling(group_list=None,group_chat=None,fleet=None):
        new_car_list,index =[],1
        new_car_list.append(f"**⛩️[{fleet[1]}|互推联盟](https://t.me/{config.get('botUserName')}/)⛩️**\n\n")
        for group in group_list:
            if group[0]!=group_chat[0]:
                link_group =await requestFleetGroupInfo(group_id=group[1],link_group=group_chat[1])
                if link_group:
                    new_car_list.append(f"**{index}: [{await truncate_string(group[3],16)}]({link_group}) \n**")
                    index += 1
                else:
                    print('链接失败')
                    continue
            else:
                continue
        new_car_list.append(f"**\nAD:[如何使用互推机器人?](https://t.me/hufen/3)**")
        new_car_list.append(f"**\n互推交流: @{config.get('publicGroup')}**")
        return new_car_list
async def convoyDriving():
    fleet_list = db.select(f"SELECT * FROM fleet_list WHERE state = 1 ")
    print('车队',fleet_list)
    if fleet_list:
        for fleet in fleet_list:
            group_list = db.select(f"SELECT * FROM group_list WHERE fleet_list=%s AND state=2",(fleet[0],))
            print('群组',group_list)
            if group_list:
                db.update("UPDATE fleet_list SET count=%s WHERE id=%s", (len(group_list), fleet[0]))
                for group in group_list:
                    Permission = await HavePermission(chatId=group[1], typeG=group[4])
                    if Permission == 1:
                        print('机器人无权限',group[3])
                        db.update("UPDATE group_list SET state=0,label='发车检查:机器人被取消了权限' WHERE id=%s", (group[0],))

                        continue
                    elif Permission == 2:
                        print('机器人未入群了',group[3])
                        db.update("UPDATE group_list SET state=0,label='发车检查:机器人未入群了' WHERE id=%s", (group[0],))
                        continue
                    getMsg = {}
                    if group[9] is not None:
                        getMsg = await app.get_messages(chat_id=group[1], message_ids=int(group[9]))
                    if not (getMsg=={} or hasattr(getMsg, 'forward_from_chat')):
                        print("未检测到上一次发送的消息")
                        db.update("UPDATE group_list SET state=0,label='发车检查:上一条消息不存在' WHERE id=%s", (text_list[0],))
                    text_list = await marshalling(group_list=group_list,group_chat=group,fleet=fleet)
                    # print('返回的文字',text_list)
                    if len(text_list)>2:
                        keyboard = [[InlineKeyboardButton("➕ 参加互推", url=f"https://t.me/{config['botUserName']}")]]
                        msg = await app.send_message(chat_id=group[1], text=''.join(text_list),
                                                     reply_markup=InlineKeyboardMarkup(keyboard),
                                                     disable_web_page_preview=True)
                        if msg.id:
                            db.update("UPDATE group_list SET msg_id=%s WHERE id=%s", (msg.id, group[0]))
                            try:
                                if group[9] is not None:
                                    await app.delete_messages(chat_id=group[1], message_ids=int(group[9]))
                            except RPCError as e:
                                print('删除上一条消息失败')
                        else:
                            print('发送失败')
