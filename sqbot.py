from CHRLINE import *
import time,json,codecs
# default device CHROMEOS not support OpenChat.
user = json.load(codecs.open("user.json","r","utf-8"))
cl = CHRLINE("",device="IOSIPAD",useThrift = True)
events = cl.fetchMyEvents()
while True:
    try:
        events = cl.fetchMyEvents(syncToken=events[3])
        for e in events[2]:
            #print(e)
            if e[3] == 29:
                message = e[4][30][2][1]
                if message[1] in user["admin"]:
                    if message[10]=="test":
                        cl.sendSquareMessage(message[2],"penguin")
                    if message[10]=="企鵝" and message[1] == "pd5330a2054969d0b38cab03146eab11b":
                        cl.sendSquareMessage(message[2],"我在")#權限測試
                    if message[10]=="幫助":
                        ret_ = "  ~ 社群機器人 ~"
                        ret_ +=f"\n• sqinfo 查本社群資訊"
                        ret_ +=f"\n• mid @ 查標註社群id"
                        #ret_ +=f"\n• info @ "
                        ret_ +=f"\n• sqid 查自己社群id"
                        ret_ +=f"\n• kick @ 踢人"
                        ret_ +=f"\n• 加權限/刪權限/權限表"
                        cl.sendSquareMessage(message[2],ret_)#權限測試
                    if message[10].startswith("mid ") and "MENTION" in message[18]: #標註查mid
                                mlists = []
                                key = eval(message[18]["MENTION"])
                                tags = key["MENTIONEES"]
                                for tag in tags:
                                    mid = tag['M']
                                    cl.sendMessage(message[2],str(mid))
                    if message[10].startswith("info ") and "MENTION" in message[18]: #標註查mid
                                mlists = []
                                key = eval(message[18]["MENTION"])
                                tags = key["MENTIONEES"]
                                for tag in tags:
                                    mid = tag['M']
                                    abc=cl.getSquareMember(mid)
                                    cl.sendMessage(message[2],str(abc[1][3]))
                    if message[10].startswith("kick ") and "MENTION" in message[18]: #標註kick
                                mlists = []
                                aaa=cl.getSquareChat(message[2])[1][2]
                                key = eval(message[18]["MENTION"])
                                tags = key["MENTIONEES"]
                                for tag in tags:
                                    mid = tag['M']
                                    #cl.sendMessage(message[2],str(mid))
                                    cl.deleteOtherFromSquare(aaa,str(mid))
                    if message[10]=="sqid":
                        cl.sendSquareMessage(message[2],str(message[1]))
                    if message[10]=="sqgid":
                        cl.sendSquareMessage(message[2],str(message[2]))
                    if message[10]=="sqinfo":
                        #cl.sendSquareMessage(message[2],str(message[2]))
                        sqinfo=cl.getSquareChat(message[2])
                        aaa=cl.getSquareChat(message[2])[1][2]
                        info=cl.getSquare(aaa).square#name 社群名
                        info2=cl.getSquare(aaa).squareStatus
                        ret_ = "          ~ 社群資料 ~"
                        ret_ +=f"\n• 社群名稱\n{info.name}"
                        ret_ +=f"\n• 社群介紹\n{info.desc}"
                        ret_ +=f"\n• 社群ID\n{info.mid}"
                        ret_ +=f"\n• 社群網址\n{info.invitationURL}"
                        ret_ +=f"\n• 社群人數\n{info2.memberCount}"
                        ret_ +=f"\n• 人數上限\n{sqinfo[1][7]}"
                        ret_ +=f"\n• 創建時間\n{time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(round(info.createdAt/1000))))}"
                        cl.sendSquareMessage(message[2],str(ret_))
                        #cl.sendSquareMessage(message[2],str(info2))
                    if message[10].startswith('加權限 ') and "MENTION" in message[18]:
                            suc, fail, ret_, ret_2 = [], [], "【新增權限成功】", "\n【新增權限失敗】"
                            tags = eval(message[18]["MENTION"])
                            for tag in tags["MENTIONEES"]:
                                if tag["M"] not in user["admin"]:user["admin"].append(tag["M"]);suc.append(tag["M"])
                                else:fail.append(tag["M"])
                            if not suc:ret_ += '\n • 沒有名單'
                            else:
                                for x, mid in enumerate(suc):a = cl.getSquareMember(mid);ret_ += f'\n{x+1}.{a[1][3]}'
                            if not fail:ret_2 += '\n • 沒有名單'
                            else:
                                for x, mid in enumerate(fail):a = cl.getSquareMember(mid);ret_2 += f'\n{x+1}.{a[1][3]}'
                            cl.sendSquareMessage(message[2],f'{ret_}{ret_2}')
                    if message[10].startswith('刪權限 ') and "MENTION" in message[18]:
                            suc, fail, ret_, ret_2 = [], [], "【刪除權限成功】", "\n【刪除權限失敗】"
                            tags = eval(message[18]["MENTION"])
                            for tag in tags["MENTIONEES"]:
                                if tag["M"] in user["admin"]:user["admin"].remove(tag["M"]);suc.append(tag["M"])
                                else:fail.append(tag["M"])
                            if not suc:ret_ += '\n • 沒有名單'
                            else:
                                for x, mid in enumerate(suc):a = cl.getSquareMember(mid);ret_ += f'\n{x+1}.{a[1][3]}'
                            if not fail:ret_2 += '\n • 沒有名單'
                            else:
                                for x, mid in enumerate(fail):a = cl.getSquareMember(mid);ret_2 += f'\n{x+1}.{a[1][3]}'
                            cl.sendSquareMessage(message[2],f'{ret_}{ret_2}')                    
                    if message[10] in ['權限表','權限名單','權限者']:
                            if not user["admin"]:cl.sendSquareMessage(message[2],'沒有權限者') 
                            else:
                                mc = "[權限名單如下]"
                                no = 0
                                for mid in user["admin"]:
                                    try:
                                        a = cl.getSquareMember(mid)
                                        no += 1
                                        mc += "\n{}.".format(str(no))+a[1][3]
                                    except:
                                        user["admin"].remove(mid)
                                cl.sendSquareMessage(message[2],f'{mc}\n總共{len(user["admin"])}個人在權限名單')
                    if message[10]=="sqs":
                        cl.sendSquareMessage(message[2],str(cl.getJoinedSquares()))
    except Exception as e:print(str(e))

            


