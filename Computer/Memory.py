Byte = int
Word = int
u32 = int
s32 = int

class Mem:
    def __init__(self):
        self.MAX_MEM: u32 = 1024 * 64
        self.Data = [0] * self.MAX_MEM

    def __getitem__(self, address: Byte) -> int:
        return self.Data[address & 0xFFFF]
    
    def __setitem__(self, address: Byte, value: int):
        self.Data[address & 0xFFFF] = value

    def init(self):
        self.Data = [0] * self.MAX_MEM

    def WriteWord(self, cycles: list, address: u32, data: Word):
        self.Data[address]     = data & 0xFF
        self.Data[address + 1] = (data >> 8)
        cycles[0] -= 2

