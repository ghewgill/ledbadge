import struct

ACTION_HOLD = 'A'
ACTION_ROTATE = 'B'
ACTION_SNOW = 'C'
ACTION_FLASH = 'D'
ACTION_HOLDFRAME = 'E'

class Packet:
    def __init__(self, command, address, data):
        self.command = command
        self.address = address
        self.data = data

    def format(self):
        if self.command == '3':
            return struct.pack("BcB", 2, self.command, self.data)
        else:
            buf = struct.pack(">BcH64s",
                2,
                self.command,
                self.address,
                self.data)
            buf += chr(sum(map(ord, buf[1:])) & 0xff)
            return buf

def build_packets(address, data):
    r = []
    command = '1'
    for i in range(0, len(data), 64):
        p = Packet(command, address, data[i:i+64])
        r.append(p)
        command = '2'
        address += 0x40
    r.append(Packet('3', 0, 0x01))
    return r

def message_file(text, speed='1', name='1', action=ACTION_HOLD):
    return struct.pack("cccB", speed, name, action, len(text)) + text

def test():
    assert "11A\x04AAAA" == message_file("AAAA")
    assert "51B\x460000000000111111111122222222223333333333444444444455555555556666666666" == message_file("0000000000111111111122222222223333333333444444444455555555556666666666", speed='5', action=ACTION_ROTATE)
    pkts = build_packets(0x600, message_file("0000000000111111111122222222223333333333444444444455555555556666666666777777777788888888889999999999aaaaaaaaaa", speed='5', action=ACTION_ROTATE))
    assert 3 == len(pkts)
    assert "\x02\x31\x06\x0051B\x6e000000000011111111112222222222333333333344444444445555555555#" == pkts[0].format()
    assert "\x02\x32\x06\x406666666666777777777788888888889999999999aaaaaaaaaa\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xee" == pkts[1].format()
    assert "\x02\x33\x01" == pkts[2].format()

if __name__ == "__main__":
    test()
