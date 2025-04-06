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
        self.assertIn(CyclesUsed, [4, 5])  # Page crossing possible
        self.assertFalse(self.cpu.Z_flag)
        self.assertTrue(self.cpu.N_flag)
        self.VerifyFlags_NoMod_LDA()

    def test_LDA_ABSX_Wrap(self):
        self.cpu.X_reg = 0x0F
        self.mem[0xFFFC] = self.cpu.INS_LDA_ABSX
        self.mem[0xFFFD] = 0xF5
        self.mem[0xFFFE] = 0xFF
        self.mem[(0xFFF5 + self.cpu.X_reg) & 0xFFFF] = 0x84
        CyclesUsed = self.cpu.exec(self.mem, 4)
        self.assertEqual(self.cpu.A_reg, 0x84)
        self.assertIn(CyclesUsed, [4, 5])
        self.assertFalse(self.cpu.Z_flag)
        self.assertTrue(self.cpu.N_flag)
        self.VerifyFlags_NoMod_LDA()

    def test_NOP_IF_CYCLES_EQ_0(self):
        CyclesUsed = self.cpu.exec(self.mem, 0)
        self.assertEqual(CyclesUsed, 0)

    def test_LDA_IM_LT_NC(self):
        self.mem[0xFFFC] = self.cpu.INS_LDA_IM
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
