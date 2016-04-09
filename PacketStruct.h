struct C2GM_test {
    uint32 id;
    int32 sex;
    int age;
    string name;
    std::vector<AccountInfo> vecInt;
    std::map<int,PlayerInfo> mapHis;
    void ToPacket(INetPacket& packet)
    {
        packet << id;
        packet << sex;
        packet << age;
        packet << name;
        packet << (uint32)vecInt.size();
        for(int i = 0; i < vecInt.size(); i++)
        {
            vecInt.ToPacket(packet);
        }
        packet << (uint32)mapHis.size();
        std::map<int,PlayerInfo>::iterator it = mapHis.begin; it != mapHis.end(); it++)
        {
            packet << it->first;
            it->second.ToPacket(packet);
        }
    }
    void FromPacket(INetPacket& packet)
    {
        int size;
        packet >> id;
        packet >> sex;
        packet >> age;
        packet >> name;
        packet >> size;
        for(int i = 0; i < size; i++)
        {
            AccountInfo info;
            info.FromPacket(packet);
            vecInt.push_back(info);
        }
        packet >> size;
        for(int i = 0; i < size; i++)
        {
            int key;
            PlayerInfo value;
            packet >> key;
            value.FromPacket(packet);
            mapHis.insert(make_pair(key,value));
        }
    }
}
