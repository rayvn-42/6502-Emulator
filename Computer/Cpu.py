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
        '''(Load A zero page, X) Loads a value into the A register from the ZP address + value in X register,    Cycles: 4'''
        self.INS_LDA_ABS: Byte = 0xAD
        '''(Load A absolute) Loads a value into the A register using a 16-bit address,    Cycles: 4'''
        self.INS_LDA_ABSX: Byte = 0xBD
        '''(Load A absolute, X) Loads a value into the A register using a 16-bit address + value in X register,    Cycles: 4 (+1 if page crossed)'''
        self.INS_LDA_ABSY: Byte = 0xB9
        '''(Load A absolute, Y) Loads a value into the A register using a 16-bit address + value in Y register,    Cycles: 4 (+1 if page crossed)'''
        self.INS_LDA_INDX: Byte = 0xA1
        '''(Load A indirect X) Loads a value into the A register using a ZP pointer = ZP address + value in X register, Cycles: 6'''
        self.INS_LDA_INDY: Byte = 0xB1
        '''(Load A indirect Y) Loads a value into the A register using a ZP pointer = ZP address + value in Y register, Cycles: 5 (+1 if page crossed)'''
        self.INS_LDX_IM: Byte = 0xA2
        '''(Load X immediate) Loads a value into the X register,    Cycles: 2'''
        self.INS_LDX_ZP: Byte = 0xA6
        '''(Load X zero page) Loads a value into the X register from the zero page,    Cycles: 3'''
        self.INS_LDX_ZPY: Byte = 0xB6
        '''(Load X zero page, Y) Loads a value into the X register from the ZP address + value in Y register,    Cycles: 4'''
        self.INS_LDX_ABS: Byte = 0xAE
        '''(Load X absolute) Loads a value into the X register using a 16-bit address,    Cycles: 4'''
        self.INS_LDX_ABSY: Byte = 0xBE
        '''(Load X absolute, Y) Loads a value into the X register using a 16-bit address + value in Y register,    Cycles: 4 (+1 if page crossed)'''
        self.INS_LDY_IM: Byte = 0xA0
        '''(Load Y immediate) Loads a value into the Y register,    Cycles: 2'''
        self.INS_LDY_ZP: Byte = 0xA4
        '''(Load Y zero page) Loads a value into the Y register from the zero page,    Cycles: 3'''
        self.INS_LDY_ZPX: Byte = 0xB4
        '''(Load Y zero page, X) Loads a value into the Y register from the ZP address + value in X register,    Cycles: 4'''
        self.INS_LDY_ABS: Byte = 0xAC
        '''(Load Y absolute) Loads a value into the Y register using a 16-bit address,    Cycles: 4'''
        self.INS_LDY_ABSX: Byte = 0xBC
        '''(Load Y absolute, X) Loads a value into the Y register using a 16-bit address + value in X register,    Cycles: 4 (+1 if page crossed)'''
        self.INS_STA_ZP: Byte = 0x85
        '''(Store A zero page) Stores the contents of the A register into zero page,    Cycles: 3'''
        self.INS_STA_ZPX: Byte = 0x95
        '''(Store A zero page, X) Stores the contents of the A register into zero page + value in X register,    Cycles: 4'''
        self.INS_STA_ABS: Byte = 0x8D
        '''(Store A absolute) Stores the contents of the A register into memory using a 16-bit address,    Cycles: 4'''
        self.INS_STA_ABSX: Byte = 0x9D
        '''(Store A absolute, X) Stores the contents of the A register into memory using a 16-bit address + value in X register,    Cycles: 5'''
        self.INS_STA_ABSY: Byte = 0x99
        '''(Store A absolute, Y) Stores the contents of the A register into memory using a 16-bit address + value in Y register,    Cycles: 5'''
        self.INS_STA_INDX: Byte = 0x81
        '''(Store A indirect X) Stores the contents of the A register into memory using a ZP pointer = ZP address + value in X register, Cycles: 6'''
        self.INS_STA_INDY: Byte = 0x91
        '''(Store A indirect Y) Stores the contents of the A register into memory using a ZP pointer = ZP address + value in Y register, Cycles: 5 (+1 if page crossed)'''
        self.INS_STX_ZP: Byte = 0x86
        '''(Store X zero page) Stores the contents of the X register into zero page,    Cycles: 3'''
        self.INS_STX_ZPY: Byte = 0x96
        '''(Store X zero page, Y) Stores the contents of the X register into zero page + value in Y register,    Cycles: 4'''
        self.INS_STX_ABS: Byte = 0x8E
        '''(Store X absolute) Stores the contents of the X register into memory using a 16-bit address,    Cycles: 4'''
        self.INS_STY_ZP: Byte = 0x84
        '''(Store Y zero page) Stores the contents of the Y register into zero page,    Cycles: 3'''
        self.INS_STY_ZPX: Byte = 0x94
        '''(Store Y zero page, X) Stores the contents of the Y register into zero page + value in X register,    Cycles: 4'''
        self.INS_STY_ABS: Byte = 0x8C
        '''(Store Y absolute) Stores the contents of the Y register into memory using a 16-bit address,    Cycles: 4'''
        self.INS_TAX_IMP: Byte = 0xAA
        '''(Transfer A to X) Transfers the value in A register to X register, Cycles: 2'''
        self.INS_TAY_IMP: Byte = 0xA8
        '''(Transfer A to Y) Transfers the value in A register to Y register, Cycles: 2'''
        self.INS_TSX_IMP: Byte = 0xBA
        '''(Transfer stack to X) Transfers the value in the stack to X register, Cycles: 2'''
        self.INS_TXA_IMP: Byte = 0x8A
        '''(Transfer X to A) Transfers the value in X register to A register, Cycles: 2'''
        self.INS_TXS_IMP: Byte = 0x9A
        '''(Transfer X to stack) Transfers the value in X register to the stack, Cycles: 2'''
        self.INS_TYA_IMP: Byte = 0x98
        '''(Transfer Y to A) Transfers the value in Y register to A register, Cycles: 2'''
        self.INS_JSR: Byte = 0x20
        '''(Jump to subroutine) Pushes an address to the stack then jumps to that address in memory    Cycles: 4'''
        self.INS_NOP: Byte = 0xEA
        '''(No operation) Increments the program counter and does nothing,    Cycles: 2'''
        self.INS_PHA: Byte = 0x48
        '''(Push A) Pushes a copy of A register on to the stack,    Cycles: 3'''
        self.INS_PHP: Byte = 0x08
        '''(Push PS) Pushes status flags on to the stack,    Cycles: 3'''
        self.INS_PLA: Byte = 0x68
        '''(Pull A) Pulls a byte from stack and into A register,    Cycles: 4'''
        self.INS_PLP: Byte = 0x28
        '''(Pull PS) Pulls a byte from stack and into the processor status,    Cycles: 4'''
        self.INS_AND_IM: Byte = 0x29
        '''(AND immediate) logical AND operation performed on the A register and an address in memory,    Cycles: 2'''
        self.INS_AND_ZP: Byte = 0x25
        '''(AND zero page) logical AND operation performed on the A register and an address in zero page,    Cycles: 3'''
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

    def ASetStatus(self):
        self.Z_flag = (True if self.A_reg == 0 else False)
        self.N_flag = (True if self.A_reg & 0b10000000 else False)
    
    def XSetStatus(self):
        self.Z_flag = (True if self.X_reg == 0 else False)
        self.N_flag = (True if self.X_reg & 0b10000000 else False)

    def YSetStatus(self):
        self.Z_flag = (True if self.Y_reg == 0 else False)
        self.N_flag = (True if self.Y_reg & 0b10000000 else False)

    def exec(self, memory: Mem, cycles: s32) -> s32:
        start_cycles: s32 = cycles
        while cycles > 0:
            cycles_lst = [cycles]
            Ins: Byte = self.fetchByte( memory, cycles_lst )
            match Ins:
                #LDA (load into A register) instruction
                case self.INS_LDA_IM:
                    Value: Byte = self.fetchByte( memory, cycles_lst )
                    self.A_reg = Value
                    self.ASetStatus()
                case self.INS_LDA_ZP:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    self.A_reg = self.readByte( memory, ZeroPageAddress, cycles_lst )
                    self.ASetStatus()
                case self.INS_LDA_ZPX:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    ZeroPageAddress = (ZeroPageAddress + self.X_reg) & 0xFF
                    cycles_lst[0] -= 1
                    self.A_reg = self.readByte( memory, ZeroPageAddress, cycles_lst )
                    self.ASetStatus()
                case self.INS_LDA_ABS:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    Address: Word = LSB_Byte | (MSB_Byte << 8)
                    self.A_reg = self.readByte( memory, Address, cycles_lst )
                    self.ASetStatus()
                case self.INS_LDA_ABSX:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    BaseAddress: Word = LSB_Byte | (MSB_Byte << 8)
                    Address: Word = BaseAddress + self.X_reg
                    if (BaseAddress & 0xFF00) != (Address & 0xFF00):
                        cycles_lst[0] -= 1
                    Value: Byte = self.readByte( memory, Address, cycles_lst )
                    self.A_reg = Value
                    self.ASetStatus()
                case self.INS_LDA_ABSY:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    BaseAddress: Word = LSB_Byte | (MSB_Byte << 8)
                    Address: Word = BaseAddress + self.Y_reg
                    if (BaseAddress & 0xFF00) != (Address & 0xFF00):
                        cycles_lst[0] -= 1
                    Value: Byte = self.readByte( memory, Address, cycles_lst )
                    self.A_reg = Value
                    self.ASetStatus()
                case self.INS_LDA_INDX:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    ZP_Pointer: Byte = (ZeroPageAddress + self.X_reg) & 0xFF
                    cycles_lst[0] -= 1
                    LSB_Byte: Byte = self.readByte( memory, ZP_Pointer, cycles_lst )
                    MSB_Byte: Byte = self.readByte( memory, (ZP_Pointer + 1) & 0xFF, cycles_lst )
                    Address: Word = (MSB_Byte << 8) | LSB_Byte
                    Value: Byte = self.readByte( memory, Address, cycles_lst )
                    self.A_reg = Value
                    self.ASetStatus()
                case self.INS_LDA_INDY:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    LSB_Byte: Byte = self.readByte( memory, ZeroPageAddress, cycles_lst )
                    MSB_Byte: Byte = self.readByte( memory, (ZeroPageAddress + 1) & 0xFF, cycles_lst )
                    BaseAddress: Word = (MSB_Byte << 8) | LSB_Byte
                    Address: Word = BaseAddress + self.Y_reg
                    if (BaseAddress & 0xFF00) != (Address & 0xFF00):
                        cycles_lst[0] -= 1
                    Value: Byte = self.readByte( memory, Address, cycles_lst )
                    self.A_reg = Value
                    self.ASetStatus()
                #LDX (load into X register) instruction
                case self.INS_LDX_IM:
                    Value: Byte = self.fetchByte( memory, cycles_lst )
                    self.X_reg = Value
                    self.XSetStatus()
                case self.INS_LDX_ZP:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    self.X_reg = self.readByte( memory, ZeroPageAddress, cycles_lst )
                    self.XSetStatus()
                case self.INS_LDX_ZPY:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    ZeroPageAddress = (ZeroPageAddress + self.Y_reg) & 0xFF
                    cycles_lst[0] -= 1
                    self.X_reg = self.readByte( memory, ZeroPageAddress, cycles_lst )
                    self.XSetStatus()
                case self.INS_LDX_ABS:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    Address: Word = LSB_Byte | (MSB_Byte << 8)
                    self.X_reg = self.readByte( memory, Address, cycles_lst )
                    self.XSetStatus()
                case self.INS_LDX_ABSY:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    BaseAddress: Word = LSB_Byte | (MSB_Byte << 8)
                    Address: Word = BaseAddress + self.Y_reg
                    if (BaseAddress & 0xFF00) != (Address & 0xFF00):
                        cycles_lst[0] -= 1
                    self.X_reg = self.readByte( memory, Address, cycles_lst )
                    self.XSetStatus()
                #LDY (load into Y register) instruction
                case self.INS_LDY_IM:
                    Value: Byte = self.fetchByte( memory, cycles_lst )
                    self.Y_reg = Value
                    self.YSetStatus()
                case self.INS_LDY_ZP:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    self.Y_reg = self.readByte( memory, ZeroPageAddress, cycles_lst )
                    self.YSetStatus()
                case self.INS_LDY_ZPX:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    ZeroPageAddress = (ZeroPageAddress + self.X_reg) & 0xFF
                    cycles_lst[0] -= 1
                    self.Y_reg = self.readByte( memory, ZeroPageAddress, cycles_lst )
                    self.YSetStatus()
                case self.INS_LDY_ABS:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    Address: Word = LSB_Byte | (MSB_Byte << 8)
                    self.Y_reg = self.readByte( memory, Address, cycles_lst )
                    self.YSetStatus()
                case self.INS_LDY_ABSX:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    BaseAddress: Word = LSB_Byte | (MSB_Byte << 8)
                    Address: Word = BaseAddress + self.X_reg
                    if (BaseAddress & 0xFF00) != (Address & 0xFF00):
                        cycles_lst[0] -= 1
                    self.Y_reg = self.readByte( memory, Address, cycles_lst )
                    self.YSetStatus()
                #JSR (jump to subroutine) instruction
                case self.INS_JSR:
                    SubAddr: Word = self.fetchWord( memory, cycles_lst )
                    self.SP -= 2
                    memory.WriteWord( cycles_lst, self.SP, self.PC - 1 )
                    self.PC = SubAddr
                    cycles_lst[0] -= 1
                #NOP (no operation) instruction
                case self.INS_NOP:
                    self.PC += 1
                    cycles_lst[0] -= 1
                #STA store into A register instruction
                case self.INS_STA_ZP:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    memory.WriteByte( cycles_lst, ZeroPageAddress & 0xFF, self.A_reg )
                case self.INS_STA_ZPX:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    Address: Byte = ZeroPageAddress + self.X_reg
                    cycles_lst[0] -= 1
                    memory.WriteByte( cycles_lst, Address & 0xFF, self.A_reg )
                case self.INS_STA_ABS:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    Address: Word = LSB_Byte | (MSB_Byte << 8)
                    memory.WriteByte( cycles_lst, Address & 0xFFFF, self.A_reg )
                case self.INS_STA_ABSX:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    BaseAddress: Word = LSB_Byte | (MSB_Byte << 8)
                    Address: Word = BaseAddress + self.X_reg
                    cycles_lst[0] -= 1
                    if (BaseAddress & 0xFF00) != (Address & 0xFF00):
                        cycles_lst[0] -= 1
                    memory.WriteByte( cycles_lst, Address, self.A_reg )
                case self.INS_STA_ABSY:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    BaseAddress: Word = LSB_Byte | (MSB_Byte << 8)
                    Address: Word = BaseAddress + self.Y_reg
                    cycles_lst[0] -= 1
                    if (BaseAddress & 0xFF00) != (Address & 0xFF00):
                        cycles_lst[0] -= 1
                    memory.WriteByte( cycles_lst, Address, self.A_reg )
                case self.INS_STA_INDX:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    ZP_Pointer: Byte = (ZeroPageAddress + self.X_reg) & 0xFF
                    cycles_lst[0] -= 1
                    LSB_Byte: Byte = self.readByte( memory, ZP_Pointer, cycles_lst )
                    MSB_Byte: Byte = self.readByte( memory, (ZP_Pointer + 1) & 0xFF, cycles_lst )
                    Address: Word = (MSB_Byte << 8) | LSB_Byte
                    memory.WriteByte( cycles_lst, Address, self.A_reg )
                case self.INS_STA_INDY:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    ZP_Pointer: Word = (ZeroPageAddress + self.Y_reg) & 0xFF
                    LSB_Byte: Byte = self.readByte( memory, ZP_Pointer, cycles_lst )
                    MSB_Byte: Byte = self.readByte( memory, (ZP_Pointer + 1) & 0xFF, cycles_lst )
                    Address: Word = (MSB_Byte << 8) | LSB_Byte
                    cycles_lst[0] -= 1
                    memory.WriteByte( cycles_lst, Address, self.A_reg )
                #STX store into X register instruction
                case self.INS_STX_ZP:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    memory.WriteByte( cycles_lst, ZeroPageAddress & 0xFF, self.X_reg )
                case self.INS_STX_ZPY:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    Address: Byte = ZeroPageAddress + self.Y_reg
                    cycles_lst[0] -= 1
                    memory.WriteByte( cycles_lst, Address & 0xFF, self.X_reg )
                case self.INS_STX_ABS:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    Address: Word = LSB_Byte | (MSB_Byte << 8)
                    memory.WriteByte( cycles_lst, Address & 0xFFFF, self.X_reg )
                #STY store into Y register instruction
                case self.INS_STY_ZP:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    memory.WriteByte( cycles_lst, ZeroPageAddress & 0xFF, self.Y_reg )
                case self.INS_STY_ZPX:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    Address: Byte = ZeroPageAddress + self.X_reg
                    cycles_lst[0] -= 1
                    memory.WriteByte( cycles_lst, Address & 0xFF, self.Y_reg )
                case self.INS_STY_ABS:
                    LSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    MSB_Byte: Byte = self.fetchByte( memory, cycles_lst )
                    Address: Word = LSB_Byte | (MSB_Byte << 8)
                    memory.WriteByte( cycles_lst, Address & 0xFFFF, self.Y_reg )
                #Transfer instructions
                case self.INS_TAX_IMP:
                    self.X_reg = self.A_reg
                    self.XSetStatus()
                    cycles_lst[0] -= 1
                case self.INS_TAY_IMP:
                    self.Y_reg = self.A_reg
                    self.YSetStatus()
                    cycles_lst[0] -= 1
                case self.INS_TSX_IMP:
                    self.X_reg = self.SP & 0xFF
                    self.XSetStatus()
                    cycles_lst[0] -= 1
                case self.INS_TXA_IMP:
                    self.A_reg = self.X_reg
                    self.ASetStatus()
                    cycles_lst[0] -= 1
                case self.INS_TXS_IMP:
                    self.SP = self.X_reg & 0xFF
                    cycles_lst[0] -= 1
                case self.INS_TYA_IMP:
                    self.A_reg = self.Y_reg
                    self.ASetStatus()
                    cycles_lst[0] -= 1
                #Push instructions
                case self.INS_PHA:
                    memory.WriteByte( cycles_lst, 0x0100 + self.SP, self.A_reg )
                    self.SP = (self.SP - 1) & 0xFF
                    cycles_lst[0] -= 1
                case self.INS_PHP:
                    Status = self.P_status | 0b00110000
                    memory.WriteByte( cycles_lst, 0x0100 + self.SP, Status )
                    self.SP = (self.SP - 1) & 0xFF
                    cycles_lst[0] -= 1
                #Pull instructions
                case self.INS_PLA:
                    self.SP = (self.SP + 1) & 0xFF
                    self.A_reg = memory[0x0100 + self.SP]
                    self.ASetStatus()
                    cycles_lst[0] -= 3
                case self.INS_PLP:
                    self.SP = (self.SP + 1) & 0xFF
                    self.P_status = (memory[0x0100 + self.SP] & 0b11001111) | 0b00100000
                    cycles_lst[0] -= 3
                #Logical instructions
                case self.INS_AND_IM:
                    Value: Byte = self.fetchByte( memory, cycles_lst )
                    self.A_reg = self.A_reg & Value
                    self.ASetStatus()
                case self.INS_AND_ZP:
                    ZeroPageAddress: Byte = self.fetchByte( memory, cycles_lst )
                    Value: Byte = self.readByte( memory, ZeroPageAddress, cycles_lst )
                    self.A_reg = self.A_reg & Value
                    self.ASetStatus()
                case _:
                    print(f"Instruction not handled: {Ins}")
                    
            cycles = cycles_lst[0]

        CYCLES_USED: s32 = start_cycles - cycles
        return CYCLES_USED