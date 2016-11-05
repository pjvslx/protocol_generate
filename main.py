#-*- coding: UTF-8 -*-
if __name__ == "__main__":
    import json
    import os
    import nf_tools
    # if os.path.exists("test.json"):
    #     os.remove("test.json")
    # else:
    #     pass
    str = '{"1":"abc", "2":"ABC"}'
    jstr = json.loads(str)
    print jstr.keys()
    print jstr["1"]

    # fp = open("test.json",'w+')
    # fp.write(str)
    # fp.close()

    # struct BABSPlayerInfo   //玩家基本信息
    # {
    #     stPlayerAccountInfo     accInfo;
    #     stPlayerCharacterInfo   charInfo;
    #     stPlayerPropTable       propInfo;
    #     int                    seatPosition;  //玩家坐下的位置(庄家、候选庄家、坐下玩家、站起玩家)
    #     int64                  bankerMoney;   //玩家上庄携币量
    #     int64                  resultMoney;   //玩家结算结果，正数为赢 负数为输
    #     std::map<int, int64>    anteInfo;      //我自己在各个禽兽上的下注信息(key--禽兽类型  value--下注金额)
    #     std::map<int, int64>    resultInfo;    //我自己在各个禽兽上的输赢信息，正数为赢 负数为输(key--禽兽类型  value--下注金额)
    #     int                   remainAutoAnteTurnNum;//玩家剩余自动跟注轮数
    #     int64                  winJackpot;    //玩家赢明池金币
    #     int                   leftResetTimes;//庄家剩余重置上庄金币次数
    #     int					 frameId;
    # }


    # [ ["accInfo","stPlayerAccountInfo"], ["charInfo","stPlayerCharacterInfo"], ["propInfo","stPlayerPropTable"], ["seatPosition","int"], ["bankerMoney","int64"],["resultMoney","int64"], ["anteInfo",["int","int64"]], ["resultInfo",["int","int64"]], ["remainAutoAnteTurnNum","int"] , ["winJackpot","int64"],["leftResetTimes","int"] , ["frameId","int"] ]
    # { "id":"uint32" , "sex" ; "int32" , "age" : "int" , "name" : "string"}

    fp = open("PacketStruct.h","w+")
    #input_str = [["id","uint32"],["sex","int32"],["age","int"],["name","string"],["vecInt",["AccountInfo"]],["mapHis",["int","PlayerInfo"]]];

    input_str = [ ["accInfo","stPlayerAccountInfo"], ["charInfo","stPlayerCharacterInfo"], ["propInfo","stPlayerPropTable"], ["seatPosition","int"], ["bankerMoney","int64"],["resultMoney","int64"], ["anteInfo",["int","int64"]], ["resultInfo",["int","int64"]], ["remainAutoAnteTurnNum","int"] , ["winJackpot","int64"],["leftResetTimes","int"] , ["frameId","int"] ]

    #nf_tools.generate_struct(fp,input_str,"C2GM_test")

    nf_tools.generate_lua_protocol(fp,input_str,"C2GM_test")