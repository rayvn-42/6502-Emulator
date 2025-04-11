import unittest
import Computer

Byte = int
Word = int
u32 = int
s32 = int

class TestComputer(unittest.TestCase):

    def setUp(self):
        self.mem = Computer.Memory.Mem()
        self.cpu = Computer.Cpu.CPU()
        self.cpu.reset(self.mem)

    def VerifyFlags_NoMod_LDA(self):
        self.assertFalse(self.cpu.I_flag)
        self.assertFalse(self.cpu.D_flag)
        self.assertFalse(self.cpu.B_flag)
        self.assertFalse(self.cpu.V_flag)
        self.assertFalse(self.cpu.C_flag)

    def VerifyFlags_NoMod_LDX(self):
        self.assertFalse(self.cpu.I_flag)
        self.assertFalse(self.cpu.D_flag)
        self.assertFalse(self.cpu.B_flag)
        self.assertFalse(self.cpu.V_flag)
        self.assertFalse(self.cpu.C_flag)

    def VerifyFlags_NoMod_LDY(self):
        self.assertFalse(self.cpu.I_flag)
        self.assertFalse(self.cpu.D_flag)
        self.assertFalse(self.cpu.B_flag)
        self.assertFalse(self.cpu.V_flag)
        self.assertFalse(self.cpu.C_flag)

    def VerifyFlags_NoMod_STA(self):
        self.assertFalse(self.cpu.Z_flag)
        self.assertFalse(self.cpu.I_flag)
        self.assertFalse(self.cpu.D_flag)
        self.assertFalse(self.cpu.B_flag)
        self.assertFalse(self.cpu.V_flag)
        self.assertFalse(self.cpu.C_flag)
        self.assertFalse(self.cpu.N_flag)

    def VerifyFlags_NoMod_STX(self):
        self.assertFalse(self.cpu.Z_flag)
        self.assertFalse(self.cpu.I_flag)
        self.assertFalse(self.cpu.D_flag)
        self.assertFalse(self.cpu.B_flag)
        self.assertFalse(self.cpu.V_flag)
        self.assertFalse(self.cpu.C_flag)
        self.assertFalse(self.cpu.N_flag)

    def VerifyFlags_NoMod_STY(self):
        self.assertFalse(self.cpu.Z_flag)
        self.assertFalse(self.cpu.I_flag)
        self.assertFalse(self.cpu.D_flag)
        self.assertFalse(self.cpu.B_flag)
        self.assertFalse(self.cpu.V_flag)
        self.assertFalse(self.cpu.C_flag)
        self.assertFalse(self.cpu.N_flag)

    def test_LDA_IM(self):
        self.mem[0xFFFC] = self.cpu.INS_LDA_IM
        self.mem[0xFFFD] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 2)
        self.assertEqual(self.cpu.A_reg, 0x84)
        self.assertEqual(CyclesUsed, 2)
        self.assertFalse(self.cpu.Z_flag)
        self.assertTrue(self.cpu.N_flag)
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_IM_ZERO(self):
        self.cpu.A_reg = 0x44
        self.mem[0xFFFC] = self.cpu.INS_LDA_IM
        self.mem[0xFFFD] = 0x00
        CyclesUsed = self.cpu.exec(self.mem, 2)
        self.assertEqual(self.cpu.A_reg, 0x00)
        self.assertEqual(CyclesUsed, 2)
        self.assertTrue(self.cpu.Z_flag)
        self.assertFalse(self.cpu.N_flag)
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_ZP(self):
        self.mem[0xFFFC] = self.cpu.INS_LDA_ZP
        self.mem[0xFFFD] = 0x42
        self.mem[0x0042] = 0x37
        CyclesUsed = self.cpu.exec(self.mem, 3)
        self.assertEqual(self.cpu.A_reg, 0x37)
        self.assertEqual(CyclesUsed, 3)
        self.assertFalse(self.cpu.Z_flag)
        self.assertFalse(self.cpu.N_flag)
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_ZPX(self):
        self.cpu.X_reg = 5
        self.mem[0xFFFC] = self.cpu.INS_LDA_ZPX
        self.mem[0xFFFD] = 0x42
        self.mem[0x0047] = 0x37
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.A_reg, 0x37)
        self.assertEqual(CyclesUsed, 4)
        self.assertFalse(self.cpu.Z_flag)
        self.assertFalse(self.cpu.N_flag)
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_ZPX_Wrap(self):
        self.cpu.X_reg = 0xFF
        self.mem[0xFFFC] = self.cpu.INS_LDA_ZPX
        self.mem[0xFFFD] = 0x80
        self.mem[0x007F] = 0x37
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.A_reg, 0x37)
        self.assertEqual(CyclesUsed, 4)
        self.assertFalse(self.cpu.Z_flag)
        self.assertFalse(self.cpu.N_flag)
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_ABS(self):
        self.mem[0xFFFC] = self.cpu.INS_LDA_ABS
        self.mem[0xFFFD] = 0x80
        self.mem[0xFFFE] = 0x44
        self.mem[0x4480] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.A_reg, 0x84)
        self.assertEqual(CyclesUsed, 4)
        self.assertFalse(self.cpu.Z_flag)
        self.assertTrue(self.cpu.N_flag)
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_ABSX(self):
        self.cpu.X_reg = 0x45
        self.mem[0xFFFC] = self.cpu.INS_LDA_ABSX
        self.mem[0xFFFD] = 0x45
        self.mem[0xFFFE] = 0x01
        self.mem[0x0145 + self.cpu.X_reg] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.A_reg, 0x84)
        self.assertIn(CyclesUsed, [4, 5])
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_ABSX_Wrap(self):
        self.cpu.X_reg = 0x0F
        self.mem[0xFFFC] = self.cpu.INS_LDA_ABSX
        self.mem[0xFFFD] = 0xF5
        self.mem[0xFFFE] = 0xFF
        self.mem[0xFFF5 + self.cpu.X_reg] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 5)
        self.assertEqual(self.cpu.A_reg, 0x84)
        self.assertIn(CyclesUsed, [4, 5])
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_ABSY(self):
        self.cpu.Y_reg = 0xA7
        self.mem[0xFFFC] = self.cpu.INS_LDA_ABSY
        self.mem[0xFFFD] = 0x87
        self.mem[0xFFFE] = 0x01
        self.mem[0x0187 + self.cpu.Y_reg] = 0x85
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.A_reg, 0x85)
        self.assertIn(CyclesUsed, [4, 5])
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_ABSY_Wrap(self):
        self.cpu.Y_reg = 0x0F
        self.mem[0xFFFC] = self.cpu.INS_LDA_ABSY
        self.mem[0xFFFD] = 0xF5
        self.mem[0xFFFE] = 0xFF
        self.mem[0xFFF5 + self.cpu.Y_reg] = 0x85
        CyclesUsed = self.cpu.exec(self.mem, 5)
        self.assertEqual(self.cpu.A_reg, 0x85)
        self.assertIn(CyclesUsed, [4, 5])
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_INDX(self):
        self.cpu.X_reg = 0x04
        self.mem[0xFFFC] = self.cpu.INS_LDA_INDX
        self.mem[0xFFFD] = 0x20
        self.mem[0x0020 + self.cpu.X_reg] = 0x34
        self.mem[(0x0020 + self.cpu.X_reg) + 0x01] = 0x12
        self.mem[0x1234] = 0x99
        CyclesUsed = self.cpu.exec(self.mem, 6)
        self.assertEqual(self.cpu.A_reg, 0x99)
        self.assertEqual(CyclesUsed, 6)
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_INDX_Wrap(self):
        self.cpu.X_reg = 0x0F
        self.mem[0xFFFC] = self.cpu.INS_LDA_INDX
        self.mem[0xFFFD] = 0xF1
        self.mem[(0x00F1 + self.cpu.X_reg) & 0xFF] = 0x34
        self.mem[((0x00F1 + self.cpu.X_reg) + 0x01) & 0xFF] = 0x12
        self.mem[0x1234] = 0x99
        CyclesUsed = self.cpu.exec(self.mem, 6)
        self.assertEqual(self.cpu.A_reg, 0x99)
        self.assertEqual(CyclesUsed, 6)
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_INDY(self):
        self.cpu.Y_reg = 0x10
        self.mem[0xFFFC] = self.cpu.INS_LDA_INDY
        self.mem[0xFFFD] = 0x20
        self.mem[0x0020] = 0x00
        self.mem[0x0021] = 0x80
        self.mem[0x8010] = 0x99
        CyclesUsed = self.cpu.exec(self.mem, 5)
        self.assertEqual(self.cpu.A_reg, 0x99)
        self.assertEqual(CyclesUsed, 5)
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_INDY_Wrap(self):
        self.cpu.Y_reg = 0xFF
        self.mem[0xFFFC] = self.cpu.INS_LDA_INDY
        self.mem[0xFFFD] = 0x20
        self.mem[0x0020] = 0xF0
        self.mem[0x0021] = 0xFF
        self.mem[0x00EF] = 0x55
        CyclesUsed = self.cpu.exec(self.mem, 6)
        self.assertEqual(self.cpu.A_reg, 0x55)
        self.assertEqual(CyclesUsed, 6)
        self.VerifyFlags_NoMod_LDA()

    def test_LDX_IM(self):
        self.mem[0xFFFC] = self.cpu.INS_LDX_IM
        self.mem[0xFFFD] = 0x99
        CyclesUsed = self.cpu.exec(self.mem, 2)
        self.assertEqual(self.cpu.X_reg, 0x99)
        self.assertEqual(CyclesUsed, 2)
        self.VerifyFlags_NoMod_LDX()

    def test_LDX_IM_ZERO(self):
        self.cpu.X_reg = 0x44
        self.mem[0xFFFC] = self.cpu.INS_LDX_IM
        self.mem[0xFFFD] = 0x00
        CyclesUsed = self.cpu.exec(self.mem, 2)
        self.assertEqual(self.cpu.X_reg, 0x00)
        self.assertEqual(CyclesUsed, 2)
        self.VerifyFlags_NoMod_LDX()

    def test_LDX_ZP(self):
        self.mem[0xFFFC] = self.cpu.INS_LDX_ZP
        self.mem[0xFFFD] = 0x42
        self.mem[0x0042] = 0x37
        CyclesUsed = self.cpu.exec(self.mem, 3)
        self.assertEqual(self.cpu.X_reg, 0x37)
        self.assertEqual(CyclesUsed, 3)
        self.VerifyFlags_NoMod_LDX()

    def test_LDX_ZPY(self):
        self.cpu.Y_reg = 5
        self.mem[0xFFFC] = self.cpu.INS_LDX_ZPY
        self.mem[0xFFFD] = 0x42
        self.mem[0x0047] = 0x37
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.X_reg, 0x37)
        self.assertEqual(CyclesUsed, 4)
        self.VerifyFlags_NoMod_LDX()

    def test_LDX_ZPY_Wrap(self):
        self.cpu.Y_reg = 0xFF
        self.mem[0xFFFC] = self.cpu.INS_LDX_ZPY
        self.mem[0xFFFD] = 0x80
        self.mem[0x007F] = 0x37
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.X_reg, 0x37)
        self.assertEqual(CyclesUsed, 4)
        self.VerifyFlags_NoMod_LDX()

    def test_LDX_ABS(self):
        self.mem[0xFFFC] = self.cpu.INS_LDX_ABS
        self.mem[0xFFFD] = 0x80
        self.mem[0xFFFE] = 0x44
        self.mem[0x4480] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.X_reg, 0x84)
        self.assertEqual(CyclesUsed, 4)
        self.VerifyFlags_NoMod_LDX()

    def test_LDX_ABSY(self):
        self.cpu.Y_reg = 0x45
        self.mem[0xFFFC] = self.cpu.INS_LDX_ABSY
        self.mem[0xFFFD] = 0x45
        self.mem[0xFFFE] = 0x01
        self.mem[0x0145 + self.cpu.Y_reg] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.X_reg, 0x84)
        self.assertIn(CyclesUsed, [4, 5])
        self.VerifyFlags_NoMod_LDX()

    def test_LDX_ABSY_Wrap(self):
        self.cpu.Y_reg = 0x0F
        self.mem[0xFFFC] = self.cpu.INS_LDX_ABSY
        self.mem[0xFFFD] = 0xF5
        self.mem[0xFFFE] = 0xFF
        self.mem[0xFFF5 + self.cpu.Y_reg] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 5)
        self.assertEqual(self.cpu.X_reg, 0x84)
        self.assertIn(CyclesUsed, [4, 5])
        self.VerifyFlags_NoMod_LDX()

    def test_LDY_IM(self):
        self.mem[0xFFFC] = self.cpu.INS_LDY_IM
        self.mem[0xFFFD] = 0x95
        CyclesUsed = self.cpu.exec(self.mem, 2)
        self.assertEqual(self.cpu.Y_reg, 0x95)
        self.assertEqual(CyclesUsed, 2)
        self.VerifyFlags_NoMod_LDY()

    def test_LDY_IM_ZERO(self):
        self.cpu.Y_reg = 0x44
        self.mem[0xFFFC] = self.cpu.INS_LDY_IM
        self.mem[0xFFFD] = 0x00
        CyclesUsed = self.cpu.exec(self.mem, 2)
        self.assertEqual(self.cpu.Y_reg, 0x00)
        self.assertEqual(CyclesUsed, 2)
        self.VerifyFlags_NoMod_LDY()

    def test_LDY_ZP(self):
        self.mem[0xFFFC] = self.cpu.INS_LDY_ZP
        self.mem[0xFFFD] = 0x42
        self.mem[0x0042] = 0x37
        CyclesUsed = self.cpu.exec(self.mem, 3)
        self.assertEqual(self.cpu.Y_reg, 0x37)
        self.assertEqual(CyclesUsed, 3)
        self.VerifyFlags_NoMod_LDY()

    def test_LDY_ZPX(self):
        self.cpu.X_reg = 5
        self.mem[0xFFFC] = self.cpu.INS_LDY_ZPX
        self.mem[0xFFFD] = 0x42
        self.mem[0x0047] = 0x37
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.Y_reg, 0x37)
        self.assertEqual(CyclesUsed, 4)
        self.VerifyFlags_NoMod_LDY()

    def test_LDY_ABS(self):
        self.mem[0xFFFC] = self.cpu.INS_LDY_ABS
        self.mem[0xFFFD] = 0x80
        self.mem[0xFFFE] = 0x44
        self.mem[0x4480] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.Y_reg, 0x84)
        self.assertEqual(CyclesUsed, 4)
        self.VerifyFlags_NoMod_LDY()

    def test_LDY_ABSX(self):
        self.cpu.X_reg = 0x45
        self.mem[0xFFFC] = self.cpu.INS_LDY_ABSX
        self.mem[0xFFFD] = 0x45
        self.mem[0xFFFE] = 0x01
        self.mem[0x0145 + self.cpu.X_reg] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.Y_reg, 0x84)
        self.assertIn(CyclesUsed, [4, 5])
        self.VerifyFlags_NoMod_LDY()

    def test_LDY_ABSX_Wrap(self):
        self.cpu.X_reg = 0x0F
        self.mem[0xFFFC] = self.cpu.INS_LDY_ABSX
        self.mem[0xFFFD] = 0xF5
        self.mem[0xFFFE] = 0xFF
        self.mem[0xFFF5 + self.cpu.X_reg] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 5)
        self.assertEqual(self.cpu.Y_reg, 0x84)
        self.assertIn(CyclesUsed, [4, 5])
        self.VerifyFlags_NoMod_LDY()

    def test_STA_ZP(self):
        self.cpu.A_reg = 0xA4
        self.mem[0xFFFC] = self.cpu.INS_STA_ZP
        self.mem[0xFFFD] = 0x42
        CyclesUsed = self.cpu.exec(self.mem, 3)
        self.assertEqual(self.mem[0x42], self.cpu.A_reg)
        self.assertEqual(CyclesUsed, 3)
        self.VerifyFlags_NoMod_STA()

    def test_STA_ZP_Wrap(self):
        self.cpu.A_reg = 0xA4
        self.mem[0xFFFC] = self.cpu.INS_STA_ZP
        self.mem[0xFFFD] = 0x100
        CyclesUsed = self.cpu.exec(self.mem, 3)
        self.assertEqual(self.mem[0x0], self.cpu.A_reg)
        self.assertEqual(CyclesUsed, 3)
        self.VerifyFlags_NoMod_STA()

    def test_STA_ZPX(self):
        self.cpu.A_reg = 0xA4
        self.cpu.X_reg = 0x15
        self.mem[0xFFFC] = self.cpu.INS_STA_ZPX
        self.mem[0xFFFD] = 0x13
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.mem[0x13 + self.cpu.X_reg], self.cpu.A_reg)
        self.assertEqual(CyclesUsed, 4)
        self.VerifyFlags_NoMod_STA()

    def test_STA_ZPX_Wrap(self):
        self.cpu.A_reg = 0xA4
        self.cpu.X_reg = 0xF1
        self.mem[0xFFFC] = self.cpu.INS_STA_ZPX
        self.mem[0xFFFD] = 0x0F
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.mem[0x0], self.cpu.A_reg)
        self.assertEqual(CyclesUsed, 4)
        self.VerifyFlags_NoMod_STA()

    def test_STA_ABS(self):
        self.cpu.A_reg = 0xA5
        self.mem[0xFFFC] = self.cpu.INS_STA_ABS
        self.mem[0xFFFD] = 0x42
        self.mem[0xFFFE] = 0x42
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.mem[0x4242], self.cpu.A_reg)
        self.assertEqual(CyclesUsed, 4)
        self.VerifyFlags_NoMod_STA()

    def test_STA_ABSX(self):
        self.cpu.X_reg = 0x14
        self.cpu.A_reg = 0x15
        self.mem[0xFFFC] = self.cpu.INS_STA_ABSX
        self.mem[0xFFFD] = 0x42
        self.mem[0xFFFE] = 0x43
        CyclesUsed = self.cpu.exec(self.mem, 5)
        self.assertEqual(self.mem[0x4342 + self.cpu.X_reg], self.cpu.A_reg)
        self.assertEqual(CyclesUsed, 5)
        self.VerifyFlags_NoMod_STA()

    def test_STA_ABSY(self):
        self.cpu.Y_reg = 0x98
        self.cpu.A_reg = 0x09
        self.mem[0xFFFC] = self.cpu.INS_STA_ABSY
        self.mem[0xFFFD] = 0x61
        self.mem[0xFFFE] = 0xf6
        CyclesUsed = self.cpu.exec(self.mem, 5)
        self.assertEqual(self.mem[0xf661 + self.cpu.Y_reg], self.cpu.A_reg)
        self.assertEqual(CyclesUsed, 5)
        self.VerifyFlags_NoMod_STA()

    def test_STA_INDX(self):
        self.cpu.X_reg = 0x42
        self.cpu.A_reg = 0x61
        self.mem[0xFFFC] = self.cpu.INS_STA_INDX
        self.mem[0xFFFD] = 0x97
        self.mem[0x0097 + self.cpu.X_reg] = 0x2A
        self.mem[(0x0097 + self.cpu.X_reg) + 0x01] = 0x25
        CyclesUsed = self.cpu.exec(self.mem, 6)
        self.assertEqual(self.mem[0x252A], self.cpu.A_reg)
        self.assertEqual(CyclesUsed, 6)
        self.VerifyFlags_NoMod_STA()

    def test_STA_INDY(self):
        self.cpu.Y_reg = 0x24
        self.cpu.A_reg = 0xE3
        self.mem[0xFFFC] = self.cpu.INS_STA_INDY
        self.mem[0xFFFD] = 0x05
        self.mem[0x0005 + self.cpu.Y_reg] = 0x06
        self.mem[(0x0005 + self.cpu.Y_reg) + 0x01] = 0xA7
        CyclesUsed = self.cpu.exec(self.mem, 6)
        self.assertEqual(self.mem[0xA706], self.cpu.A_reg)
        self.assertEqual(CyclesUsed, 6)
        self.VerifyFlags_NoMod_STA()

    def test_STX_ZP(self):
        self.cpu.X_reg = 0xC9
        self.mem[0xFFFC] = self.cpu.INS_STX_ZP
        self.mem[0xFFFD] = 0xDD
        CyclesUsed = self.cpu.exec(self.mem, 3)
        self.assertEqual(self.mem[0xDD], self.cpu.X_reg)
        self.assertEqual(CyclesUsed, 3)
        self.VerifyFlags_NoMod_STX()

    def test_STX_ZPY(self):
        self.cpu.X_reg = 0xD1
        self.cpu.Y_reg = 0x2F
        self.mem[0xFFFC] = self.cpu.INS_STX_ZPY
        self.mem[0xFFFD] = 0xCC
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.mem[0xCC + self.cpu.Y_reg], self.cpu.X_reg)
        self.assertEqual(CyclesUsed, 4)
        self.VerifyFlags_NoMod_STX()

    def test_STX_ABS(self):
        self.cpu.X_reg = 0xAE
        self.mem[0xFFFC] = self.cpu.INS_STX_ABS
        self.mem[0xFFFD] = 0x22
        self.mem[0xFFFE] = 0xE7
        CYclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.mem[0xE722], self.cpu.X_reg)
        self.assertEqual(CYclesUsed, 4)
        self.VerifyFlags_NoMod_STX()

    def test_STY_ZP(self):
        self.cpu.Y_reg = 0xBD
        self.mem[0xFFFC] = self.cpu.INS_STY_ZP
        self.mem[0xFFFD] = 0x7E
        CyclesUsed = self.cpu.exec(self.mem, 3)
        self.assertEqual(self.mem[0x7E], self.cpu.Y_reg)
        self.assertEqual(CyclesUsed, 3)
        self.VerifyFlags_NoMod_STY()

    def test_STY_ZPX(self):
        self.cpu.Y_reg = 0xD1
        self.cpu.X_reg = 0x2F
        self.mem[0xFFFC] = self.cpu.INS_STY_ZPX
        self.mem[0xFFFD] = 0xCC
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.mem[0xFB], self.cpu.Y_reg)
        self.assertEqual(CyclesUsed, 4)
        self.VerifyFlags_NoMod_STY()

    def test_STY_ABS(self):
        self.cpu.Y_reg = 0xEA
        self.mem[0xFFFC] = self.cpu.INS_STY_ABS
        self.mem[0xFFFD] = 0x17
        self.mem[0xFFFE] = 0x35
        CYclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.mem[0x3517], self.cpu.Y_reg)
        self.assertEqual(CYclesUsed, 4)
        self.VerifyFlags_NoMod_STY()

    def test_NOP(self):
        self.mem[0xFFFC] = self.cpu.INS_NOP
        CyclesUsed = self.cpu.exec(self.mem, 2)
        self.assertEqual(CyclesUsed, 2)

    def test_NOP_IF_CYCLES_EQ_0(self):
        CyclesUsed = self.cpu.exec(self.mem, 0)
        self.assertEqual(CyclesUsed, 0)

    def test_LDA_IM_LT_NC(self):
        self.mem[0xFFFC] = self.cpu.INS_LDA_IM
        self.mem[0xFFFD] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 1)
        self.assertEqual(CyclesUsed, 2)

    def test_LDX_IM_LT_NC(self):
        self.mem[0xFFFC] = self.cpu.INS_LDX_IM
        self.mem[0xFFFD] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 1)
        self.assertEqual(CyclesUsed, 2)

    def test_LDY_IM_LT_NC(self):
        self.mem[0xFFFC] = self.cpu.INS_LDY_IM
        self.mem[0xFFFD] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 1)
        self.assertEqual(CyclesUsed, 2)

    def test_INS_NH(self):
        self.mem[0xFFFC] = 0x02
        self.mem[0xFFFD] = 0x00
        CyclesUsed = self.cpu.exec(self.mem, 2)
        self.assertEqual(CyclesUsed, 2)

if __name__ == "__main__":
    unittest.main(verbosity=2)
