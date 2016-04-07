#-*- coding: UTF-8 -*-
# { "id":"uint32" , "sex" : "int32" , "age" : "int" , "name" : "string"}  vecInt : {"int"}  mapHis : [{k1,int},{k2,string
# -eb
# }]
# bool byte short int int32 uint32 int64 uint64 string
# 如果是vector<string> 则类型为*string 如果为map<x,y>

# ToPacket:
# packet << (uint32)vec.size();
# for(int i = 0; i < vec.size(); i++)
# {
#     packet << vec[i];
#
#     vec[i].ToPacket()
# }

# [["id","uint32"],["sex","int32"],["age","int"],["name","string"],["vecInt",(int)],["mapHis",[(recordId,uint32),(winMax,uint64)]] ]

import json
import os

data_type = ["uint8","int8","uint16","int16","uint32","int32","int","uint64","int64","string","bool"]

def generate_struct(fp,str,struct_name):
    head_str = "struct" + " " + struct_name + " {\n"
    fp.write(head_str)
    jstr = json.loads(str)
    for i in range(0,len(jstr.keys())):
        key = jstr.keys()[i]
        value = jstr[key]
        #   组装字段类型
        element_str = "    " + value + " " + key + ";\n"
        fp.write(element_str)

        #   组装ToPacket和FromPacket
    fp.write("    void ToPacket(INetPacket& packet)\n")
    fp.write("    {\n")

    for i in range(0,len(jstr.keys())):
        key = jstr.keys()[i]
        value = jstr[key]
        parse_element_to_packet(fp, key, value)
    fp.write("    }\n")

    fp.write("    void FromPacket(INetPacket& packet)\n")
    fp.write("    {\n")

    for i in range(0, len(jstr.keys())):
        key = jstr.keys()[i]
        value = jstr[key]
        parse_element_from_packet(fp,key,value)

    fp.write("    }\n")

    fp.write("}\n")

    fp.flush()
    fp.close()

def is_inner_type(str):
    for i in range(0,len(data_type)):
        if data_type[i] == str :
            #内置对象
            return True

    return False

def is_vector_type(str):
    if str[0] == '*' and str[1] != '*':
        return True
    return False

def is_map_type(str):
    if str[0] == '*' and str[1] == '*':
        return True
    return False

# parse each element  k is fields name  v is field type
def parse_element_to_packet(fp, k, v):
    if is_inner_type(v) == True:
        fp.write("        packet << " + k + ";\n")
    elif is_vector_type(v) == True:
        pass
    elif is_map_type(v) == True:
        pass
    else:
        fp.write("        " + k + ".ToPacket(packet);\n")

def parse_element_from_packet(fp, k, v):
    if is_inner_type(v) == True:
        fp.write("        packet >> " + k + ";\n")
    elif is_vector_type(v) == True:
        pass
    elif is_map_type(v) == True:
        pass
    else:
        fp.write("        " + k + ".FromPacket(packet);\n")