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
read_func = ["readChar","readChar","readShort","readShort","readInt","readInt","readInt","readInt64","readInt64","readString","readBool"]
write_func = ["writeChar","writeChar","writeShort","writeShort","writeInt","writeInt","writeInt","writeInt64","writeInt64","writeString","writeBool"]

def lua_type_map_to_func(type,is_read):
    for i in range(0,len(data_type)):
        if data_type[i] == type:
            if is_read == True:
                return read_func[i]
            else:
                return write_func[i]

def generate_lua_protocol(fp, str, struct_name):
    head_str = "local " + struct_name + " = class(\"" + struct_name + "\", message)\n\n"
    fp.write(head_str)
    fp.write("function " + struct_name + ":ctor()\n")
    fp.write("    self.super.ctor(self,0)\n")
    fp.write("end\n\n")

    fp.write("function " + struct_name + ":packet_to(packet)\n")
    # packet_to 的内容
    print len(str)
    for i in range(0,len(str)):
        element = str[i]
        key = element[0]
        value = element[1]
        print element, key , value
        parse_element_packet_to_lua(fp,key,value)

    fp.write("end\n\n")

    fp.write("function " + struct_name + ":to_packet(packet)\n")
    # to_packet 的内容
    for i in range(0, len(str)):
        element = str[i]
        key = element[0]
        value = element[1]
        parse_element_to_packet_lua(fp,key,value)
    fp.write("end\n\n")

    fp.write("return " + struct_name)

    fp.flush()
    fp.close()


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

def parse_element_to_packet_lua(fp, k, v):
    func_name = lua_type_map_to_func(v,False)
    #封包
    if is_inner_type(v) == True:
        fp.write("    packet:" + func_name + "(self." + k.lower() + ")\n")
    elif util.is_list(v) and len(v) == 1:#vector
        table_name = v[0].lower() + "_list"
        fp.write("    self." + table_name + " = self." + table_name + " or {}\n")
        fp.write("    local len = #self." + table_name + "\n")
        fp.write("    packet:writeInt(len)\n")
        fp.write("    for i = 1,len do\n")
        if is_inner_type(v[0]) == True:
            func_name = lua_type_map_to_func(v[0],False)
            fp.write("        packet:" + func_name + "(self." + table_name + ")\n")
            fp.write("        end\n")
        else:
            fp.write("        self." + table_name + "to_packet(packet)\n")
            fp.write("    end\n")
    elif util.is_list(v) and len(v) == 2:#map
        table_name = v[0].lower() + "_record"
        fp.write("    self." + table_name + " = self." + table_name + " or {}\n")
        #计算出record中的长度  不能简单的用#去取 要通过for k,v in pairs获得长度
        fp.write("    local len = 0\n")
        fp.write("    for k,v in pairs(self." + table_name + ") do\n")
        fp.write("        len = len + 1\n")
        fp.write("    end\n")

        fp.write("    packet:writeInt(len)\n")
        fp.write("    for k,v in pairs(self." + table_name + ") do\n")

        key_func = lua_type_map_to_func(v[0],False)
        fp.write("        packet:" + key_func + "(k)\n")

        if is_inner_type(v[1]) == True:
            func_name = lua_type_map_to_func(v[1],False)
            fp.write("        packet:" + func_name + "(v)\n")
        else:
            fp.write("        v:to_packet(packet)\n")

        fp.write("    end\n")
        pass

def parse_element_packet_to_lua(fp, k, v):
    func_name = lua_type_map_to_func(v,True)
    #解包
    if is_inner_type(v) == True:
        fp.write("    self." + k.lower() + " = packet:" + func_name + "()\n")
    elif util.is_list(v) and len(v) == 1:#vector
        fp.write("    local len = packet:readInt()\n")
        table_name = v[0].lower() + "_list"
        fp.write("    local " + table_name + " = {}\n")
        if is_inner_type(v[0]) == True:
            func_name = lua_type_map_to_func(v[0],True)
            fp.write("    local tmp = packet:" + func_name + "()\n")
            fp.write("    self." + table_name + "[#self." + table_name + " + 1] = tmp\n")
            pass
        else:
            fp.write("    for i = 1,len do\n")
            fp.write("        local tmp = require(\"lua.component.protocol." + v[0] + "\").new()\n")
            fp.write("        tmp:packet_to(packet)\n")
            fp.write("        self." + table_name + "[#self." + table_name + " + 1] = tmp\n")
            fp.write("    end\n")
            pass
    elif util.is_list(v) and len(v) == 2:#map
        fp.write("    local len = packet:readInt()\n")
        table_name = k.lower() + "_record"
        fp.write("    local " + table_name + " = {}\n")
        ##v[0] 肯定是内置对象  v[1] 不见得
        key_func = lua_type_map_to_func(v[0],True)
        fp.write("    for i = 1, len do\n")
        fp.write("        local key = packet:" + key_func + "()\n")
        if is_inner_type(v[1]) == True:
            func_name = lua_type_map_to_func(v[1],True)
            fp.write("        local value = packet:" + func_name + "()\n")
        else:
            fp.write("        local value = require(\"lua.component.protocol." + v[1] + "\").new()\n")
            fp.write("        value:packet_to(packet)\n")

        fp.write("        self." + table_name + "[key] = value\n")

        fp.write("    end\n")


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