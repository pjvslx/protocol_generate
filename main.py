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

    # { "id":"uint32" , "sex" ; "int32" , "age" : "int" , "name" : "string"}
    fp = open("PacketStruct.h","w+")
    input_str = '{ "id":"uint32" , "sex" : "int32" , "age" : "int" , "name" : "string" , "AccountInfo":"AccountInfo"}'
    nf_tools.generate_struct(fp,input_str,"C2GM_test")