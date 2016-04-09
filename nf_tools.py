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

# [["id","uint32"],["sex","int32"],["age","int"],["name","string"],["vecInt",(int)],["mapHis",(uint32,uint64)] ]

import json
import os
import util

data_type = ["uint8","int8","uint16","int16","uint32","int32","int","uint64","int64","string","bool"]

def generate_struct(fp,str,struct_name):
    head_str = "struct" + " " + struct_name + " {\n"
    fp.write(head_str)

    if type(str) != type([]):
        print "generate_struct str is not list"
        return

    for i in range(0,len(str)):
        element = str[i]
        key = element[0]
        value = element[1]

        #   组装字段类型
        if util.is_string(value) and is_inner_type(value):
            # 内部数据
            element_str = "    " + value + " " + key + ";\n"
        elif util.is_list(value) and len(value) == 1:
            # 如果为元组 则为vector
            element_str = "    " + "std::vector<" + value[0] + "> " + key + ";\n"
        elif util.is_list(value) and len(value) == 2:
            # 如果为元组 两个元素则为map
            element_str = "    " + "std::map<" + value[0] + "," + value[1] + "> " + key + ";\n"
        fp.write(element_str)
        #   组装ToPacket和FromPacket
    fp.write("    void ToPacket(INetPacket& packet)\n")
    fp.write("    {\n")

    for i in range(0,len(str)):
        element = str[i]
        key = element[0]
        value = element[1]
        parse_element_to_packet(fp, key, value)
    fp.write("    }\n")

    fp.write("    void FromPacket(INetPacket& packet)\n")
    fp.write("    {\n")
    fp.write("        int size;\n")

    for i in range(0, len(str)):
        element = str[i]
        key = element[0]
        value = element[1]
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

def parse_element_from_packet(fp, k, v):
    if is_inner_type(v) == True:
        fp.write("        packet >> " + k + ";\n")
    elif util.is_list(v) and len(v) == 1: #vector
        fp.write("        packet >> size;\n")
        fp.write("        for(int i = 0; i < size; i++)\n")
        fp.write("        {\n")
        if is_inner_type(v[0]) == True:
            fp.write("            " + v[0] + " value;\n")
            fp.write("            packet >> value;\n")
            fp.write("            " + k + ".push_back(value);\n")
        else:
            fp.write("            " + v[0] + " info;\n")
            fp.write("            info.FromPacket(packet);\n")
            fp.write("            " + k + ".push_back(info);\n")
        fp.write("        }\n")
    elif util.is_list(v) and len(v) == 2: #map
        fp.write("        packet >> size;\n")
        fp.write("        for(int i = 0; i < size; i++)\n")
        fp.write("        {\n")
        fp.write("            " + v[0] + " key;\n")
        fp.write("            " + v[1] + " value;\n")
        if is_inner_type(v[0]) == True:
            fp.write("            packet >> key;\n")
        else:
            fp.write("            key.FromPacket(packet);\n")

        if is_inner_type(v[1]) == True:
            fp.write("            packet >> value;\n")
        else:
            fp.write("            value.FromPacket(packet);\n")

        fp.write("            " + k + ".insert(make_pair(key,value));\n")
        fp.write("        }\n")
    else:
        fp.write("        " + k + ".FromPacket(packet);\n")


# parse each element  k is fields name  v is field type
def parse_element_to_packet(fp, k, v):
    if is_inner_type(v) == True:
        fp.write("        packet << " + k + ";\n")
    elif util.is_list(v) and len(v) == 1: #vector
        fp.write("        packet << (uint32)" + k + ".size();\n")
        fp.write("        for(int i = 0; i < " + k + ".size(); i++)\n")
        fp.write("        {\n")
        if is_inner_type(v[0]) == True:
            fp.write("            packet << " + k + "[i];\n")
        else:
            fp.write("            " + k + ".ToPacket(packet);\n")
        fp.write("        }\n")
    elif util.is_list(v) and len(v) == 2: #map
        fp.write("        packet << (uint32)" + k + ".size();\n")
        fp.write("        std::map<" + v[0] + "," + v[1] + ">::iterator it = " + k + ".begin; it != " + k + ".end(); it++)\n")
        fp.write("        {\n")
        if is_inner_type(v[0]) == True:
            #内置对象
            fp.write("            packet << it->first;\n")
        else:
            #自定义对象
            fp.write("            it->first.ToPacket(packet);\n")

        if is_inner_type(v[1]) == True:
            #内置对象
            fp.write("            packet << it->second;\n")
        else:
            #自定义对象
            fp.write("            it->second.ToPacket(packet);\n")
        fp.write("        }\n")
    else:
        fp.write("        " + k + ".ToPacket(packet);\n")