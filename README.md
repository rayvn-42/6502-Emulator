# 6502 CPU Emulator

A custom emulator of the 8-bit MOS Technology 6502 processor, written in Python.
This project aims to replicate the instruction set, memory architecture, and cycle-accurate behavior of the original chip.

## Features

- Instruction set decoding
- Support for various addressing mode (Immediate, Zero Page, Absolute, Indexed)
- Emulation of CPU registers and flags

**NOTE** - This project is still under development and is heavily subject to changes, there are many vital instruction missing, and the computer is being heavily tested.

## Architecture Overview

### Components

- `Memory.py` - Emulates 64KB of memory, can handle read/write operations.
- `Cpu.py` - Contains the core CPU class, Basically the 6502 part.
- `main.py` - Entry point for unit testing (temporary) and future assembly handling and integrations

### Memory Map

- `0x0000 - 0x00FF` - Zero Page (Const)
- `0x0100 - 0x01FF` - Stack (Const)

## Getting Started

### Prerequisites

Requirements to install and run the program:
- [Python](https://www.python.org/downloads/) [Recommended: v3.12.6]
- [git](https://git-scm.com/downloads) [Recommended: v2.48.1]

### Installation

#### Option 1: using Git
1. Clone the repository
```bash
git clone https://github.com/rayvn-42/6502-Emulator.git
cd 6502-Emulator
```
#### Option 2: From Webpage
1. In the main repo page you should see a green button with `<> Code ▽` on it click it, click `Download ZIP`, And the ZIP folder should download, when finished, extract the ZIP, then open terminal window and navigate to the unzipped file directory.

For now really all you can do is run tests, but if you're a bit experienced you can modify the code to run different instruction, I mean even if you're not experienced you can give it a try. You can always redownload everything.

After installing, run:

```bash
python main.py
```

If the code is unmodified, you should see something like this:
```bash
test_INS_NH (__main__.TestComputer.test_INS_NH) ... Instruction not handled: 2
Instruction not handled: 0
ok
test_LDA_ABS (__main__.TestComputer.test_LDA_ABS) ... ok
test_LDA_ABSX (__main__.TestComputer.test_LDA_ABSX) ... ok
test_LDA_ABSX_Wrap (__main__.TestComputer.test_LDA_ABSX_Wrap) ... ok
test_LDA_ABSY (__main__.TestComputer.test_LDA_ABSY) ... ok
test_LDA_ABSY_Wrap (__main__.TestComputer.test_LDA_ABSY_Wrap) ... ok
test_LDA_IM (__main__.TestComputer.test_LDA_IM) ... ok
test_LDA_IM_LT_NC (__main__.TestComputer.test_LDA_IM_LT_NC) ... ok
test_LDA_IM_ZERO (__main__.TestComputer.test_LDA_IM_ZERO) ... ok
test_LDA_INDX (__main__.TestComputer.test_LDA_INDX) ... ok
test_LDA_INDX_Wrap (__main__.TestComputer.test_LDA_INDX_Wrap) ... ok
test_LDA_INDY (__main__.TestComputer.test_LDA_INDY) ... ok
test_LDA_INDY_Wrap (__main__.TestComputer.test_LDA_INDY_Wrap) ... ok
test_LDA_ZP (__main__.TestComputer.test_LDA_ZP) ... ok
test_LDA_ZPX (__main__.TestComputer.test_LDA_ZPX) ... ok
test_LDA_ZPX_Wrap (__main__.TestComputer.test_LDA_ZPX_Wrap) ... ok
test_LDX_ABS (__main__.TestComputer.test_LDX_ABS) ... ok
test_LDX_ABSY (__main__.TestComputer.test_LDX_ABSY) ... ok
test_LDX_ABSY_Wrap (__main__.TestComputer.test_LDX_ABSY_Wrap) ... ok
test_LDX_IM (__main__.TestComputer.test_LDX_IM) ... ok
test_LDX_IM_LT_NC (__main__.TestComputer.test_LDX_IM_LT_NC) ... ok
test_LDX_IM_ZERO (__main__.TestComputer.test_LDX_IM_ZERO) ... ok
test_LDX_ZP (__main__.TestComputer.test_LDX_ZP) ... ok
test_LDX_ZPY (__main__.TestComputer.test_LDX_ZPY) ... ok
test_LDX_ZPY_Wrap (__main__.TestComputer.test_LDX_ZPY_Wrap) ... ok
test_LDY_ABS (__main__.TestComputer.test_LDY_ABS) ... ok
test_LDY_ABSX (__main__.TestComputer.test_LDY_ABSX) ... ok
test_LDY_ABSX_Wrap (__main__.TestComputer.test_LDY_ABSX_Wrap) ... ok
test_LDY_IM (__main__.TestComputer.test_LDY_IM) ... ok
test_LDY_IM_LT_NC (__main__.TestComputer.test_LDY_IM_LT_NC) ... ok
test_LDY_IM_ZERO (__main__.TestComputer.test_LDY_IM_ZERO) ... ok
test_LDY_ZP (__main__.TestComputer.test_LDY_ZP) ... ok
test_LDY_ZPX (__main__.TestComputer.test_LDY_ZPX) ... ok
test_NOP (__main__.TestComputer.test_NOP) ... ok
test_NOP_IF_CYCLES_EQ_0 (__main__.TestComputer.test_NOP_IF_CYCLES_EQ_0) ... ok
test_STA_ABS (__main__.TestComputer.test_STA_ABS) ... ok
test_STA_ABSX (__main__.TestComputer.test_STA_ABSX) ... Instruction not handled: 0
ok
test_STA_ZP (__main__.TestComputer.test_STA_ZP) ... ok
test_STA_ZPX (__main__.TestComputer.test_STA_ZPX) ... ok
test_STA_ZPX_Wrap (__main__.TestComputer.test_STA_ZPX_Wrap) ... ok
test_STA_ZP_Wrap (__main__.TestComputer.test_STA_ZP_Wrap) ... ok

----------------------------------------------------------------------
Ran 41 tests in 0.038s

OK
```

## Contributing

### To contribute to this project:
-    Fork this repository
-    Make your changes
-    Send a pull request to add the changes to the main repository

For more information on contributing, consider looking at the [CONTRIBUTION.md](CONTRIBUTION.md) file.

## Authors

  - **Rayan Berrabah** -
    [Github](https://github.com/rayvn-42)

## License

This project is licensed under the [MIT](LICENSE)
 License - see the [LICENSE](LICENSE) file for
details

# NOTE
THIS PROJECT IS STILL UNDER DEVELOPMENT, AND IS NOT READY FOR STANDARD USE.
