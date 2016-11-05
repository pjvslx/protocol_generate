--
-- Created by IntelliJ IDEA.
-- User: zhqgan
-- Date: 11/4/2016
-- Time: 3:31 PM
-- To change this template use File | Settings | File Templates.
--
local testdef = class("testdef")

function testdef:ctor()

end

function testdef:packet_to(packet)
    self.id = packet:readInt()
    self.name = packet:readString()
    self.tb_tmp = {}
    local len = packet:readInt()

end

function testdef:to_packet(packet)

end

return testdef
