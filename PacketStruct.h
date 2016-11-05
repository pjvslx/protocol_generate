local C2GM_test = class("C2GM_test", message)

function C2GM_test:ctor()
    self.super.ctor(self,0)
end

function C2GM_test:packet_to(packet)
    self.seatposition = packet:readInt()
    self.bankermoney = packet:readInt64()
    self.resultmoney = packet:readInt64()
    local len = packet:readInt()
    local anteinfo_record = {}
    for i = 1, len do
        local key = packet:readInt()
        local value = packet:readInt64()
        self.anteinfo_record[key] = value
    end
    local len = packet:readInt()
    local resultinfo_record = {}
    for i = 1, len do
        local key = packet:readInt()
        local value = packet:readInt64()
        self.resultinfo_record[key] = value
    end
    self.remainautoanteturnnum = packet:readInt()
    self.winjackpot = packet:readInt64()
    self.leftresettimes = packet:readInt()
    self.frameid = packet:readInt()
end

function C2GM_test:to_packet(packet)
    packet:writeInt(self.seatposition)
    packet:writeInt64(self.bankermoney)
    packet:writeInt64(self.resultmoney)
    self.int_record = self.int_record or {}
    local len = 0
    for k,v in pairs(self.int_record) do
        len = len + 1
    end
    packet:writeInt(len)
    for k,v in pairs(self.int_record) do
        packet:writeInt(k)
        packet:writeInt64(v)
    end
    self.int_record = self.int_record or {}
    local len = 0
    for k,v in pairs(self.int_record) do
        len = len + 1
    end
    packet:writeInt(len)
    for k,v in pairs(self.int_record) do
        packet:writeInt(k)
        packet:writeInt64(v)
    end
    packet:writeInt(self.remainautoanteturnnum)
    packet:writeInt64(self.winjackpot)
    packet:writeInt(self.leftresettimes)
    packet:writeInt(self.frameid)
end

return C2GM_test