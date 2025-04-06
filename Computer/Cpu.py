from sys import byteorder
from . import Memory

Byte = int
Word = int
u32 = int
s32 = int
Mem = Memory.Mem

class CPU:
    def __init__(self, PC: Word = 0x0000, SP: Word = 0x0000, A_reg: Byte = 0x00, X_reg: Byte = 0x00, Y_reg: Byte = 0x00):
        self.PC = PC
        self.SP = SP
        self.A_reg, self.X_reg, self.Y_reg = A_reg, X_reg, Y_reg
        self.P_status = 0b00100000
        self.INS_LDA_IM: Byte = 0xA9
        '''(Load A immediate) Loads a value into the A register,    Cycles: 2'''
        self.INS_LDA_ZP: Byte = 0xA5
        '''(Load A zero page) Loads a value into the A register from the zero page,    Cycles: 3'''
        self.INS_LDA_ZPX: Byte = 0xB5
        '''(Load A zero page X) Loads a value into the A register from the ZP address + value in X register,    Cycles: 4'''
        self.INS_LDA_ABS: Byte = 0xAD
        '''(Load A absolute) Loads a value into the A register using a 16-bit address,    Cycles: 4'''
        self.INS_LDA_ABSX: Byte = 0xBD
        '''(Load A absolute, X) Loads a value into the A register using a 16-bit address + value in X register,    Cycles: 4 (+1 if page crossed)'''
        self.INS_JSR: Byte = 0x20
        '''(Jump to subroutine) Pushes an address to the stack then jumps to that address in memory    Cycles: 4'''
        self.PLATFORM_BIG_ENDIAN = (False if byteorder == "little" else True)

    def get_flag(self, bit: int) -> int:
        """Get the value of a specific flag (0 or 1)."""
        return (self.P_status >> bit) & 1

    def set_flag(self, bit: int, value: bool):
        """Set (1) or clear (0) a specific flag."""
        if value:
            self.P_status |= (1 << bit)
        else:
            self.P_status &= ~(1 << bit)

    # --- Properties for flags ---
    @property
    def C_flag(self): return self.get_flag(0)  # Carry
    @C_flag.setter
    def C_flag(self, value): self.set_flag(0, value)

    @property
    def Z_flag(self): return self.get_flag(1)  # Zero
    @Z_flag.setter
    def Z_flag(self, value): self.set_flag(1, value)

    @property
    def I_flag(self): return self.get_flag(2)  # Interrupt Disable
    @I_flag.setter
    def I_flag(self, value): self.set_flag(2, value)

    @property
    def D_flag(self): return self.get_flag(3)  # Decimal Mode
    @D_flag.setter
    def D_flag(self, value): self.set_flag(3, value)

    @property
    def B_flag(self): return self.get_flag(4)  # Break
    @B_flag.setter
    def B_flag(self, value): self.set_flag(4, value)

    @property
    def V_flag(self): return self.get_flag(6)  # Overflow
    @V_flag.setter
    def V_flag(self, value): self.set_flag(6, value)

    @property
    def N_flag(self): return self.get_flag(7)  # Negative
    @N_flag.setter
    def N_flag(self, value): self.set_flag(7, value)

    '''
    def test(self):
        """Print all flag values in order: C_flag, Z_flag, I_flag, D_flag, B_flag, V_flag, N_flag."""
        print(self.C_flag, self.Z_flag, self.I_flag, self.D_flag, self.B_flag, self.V_flag, self.N_flag)
    '''

    def reset(self, memory: Mem):
        self.PC = 0xFFFC
        self.SP = 0x0100
        self.C_flag = self.Z_flag = self.I_flag = self.D_flag = self.B_flag = self.V_flag = self.N_flag = 0
        self.A_reg = self.X_reg = self.Y_reg = 0
        memory.init()

    def swapBytesInWord(self, Data: Word):
        return ((Data & 0xFF) << 8) | ((Data >> 8) & 0xFF)

    def fetchByte(self, memory: Mem, cycles: list) -> Byte:
        Data: Byte = memory[self.PC]
        self.PC += 1
        cycles[0] -= 1

        return Data
    
    def fetchWord(self, memory: Mem, cycles: list) -> Word:
        low_byte: Word = memory[self.PC]
        self.PC += 1

        high_byte: Word = memory[self.PC]
        self.PC += 1

        Data: Word = (high_byte << 8) | low_byte
        cycles[0] -= 2

        if self.PLATFORM_BIG_ENDIAN:
            Data = self.swapBytesInWord(Data)

        return Data
    
    def readByte(self, memory: Mem, address: u32, cycles: list) -> Byte:
        Data: Byte = memory[address]
        cycles[0] -= 1

        return Data

    def LDASetStatus(self):
        self.Z_flag = (True if self.A_reg == 0 else False)
        self.N_flag = (True if self.A_reg & 0b10000000 else False)

    def exec(self, memory: Mem, cycles: s32) -> s32:
        start_cycles: s32 = cycles
        while cycles > 0:
            cycles_lst = [cycles]
            Ins: Byte = self.fetchByte( memory, cycles_lst )
            match Ins:
                case self.INS_LDA_IM:
                    Value: Byte = self.fetchByte( memory, cycles_lst )
                    self.A_reg = Value
                    self.LDASetStatus()
                case self.INS_LDA_ZP:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    self.A_reg = self.readByte( memory, ZeroPageAddress, cycles_lst )
                    self.LDASetStatus()
                case self.INS_LDA_ZPX:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    ZeroPageAddress = (ZeroPageAddress + self.X_reg) & 0xFF
                    cycles_lst[0] -= 1
                    self.A_reg = self.readByte( memory, ZeroPageAddress, cycles_lst )
                    self.LDASetStatus()
                case self.INS_LDA_ABS:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    Address: Word = LSB_Byte | (MSB_Byte << 8)
                    self.A_reg = self.readByte( memory, Address, cycles_lst )
                    self.LDASetStatus()
                case self.INS_LDA_ABSX:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    BaseAddress: Word = LSB_Byte | (MSB_Byte << 8)
                    Address: Word = BaseAddress + self.X_reg
                    if (BaseAddress & 0xFF00) != (Address & 0xFF00):
                        cycles_lst[0] -= 1
                    Value: Byte = self.readByte( memory, Address, cycles_lst )
                    self.A_reg = Value
                    self.LDASetStatus()
                case self.INS_JSR:
                    SubAddr: Word = self.fetchWord( memory, cycles_lst )
                    self.SP -= 2
                    memory.WriteWord( cycles_lst, self.SP, self.PC - 1 )
                    self.PC = SubAddr
                    cycles_lst[0] -= 1
                case _:
                    print(f"Instruction not handled: {Ins}")
                    
            cycles = cycles_lst[0]

        CYCLES_USED: s32 = start_cycles - cycles
        return CYCLES_USED