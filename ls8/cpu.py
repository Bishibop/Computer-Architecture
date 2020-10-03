"""CPU functionality."""

import sys


class OpDispatch:
    def __init__(self, cpu):
        self.cpu = cpu
        self.reg = cpu.reg

    def execute(self, op_code, operand_a, operand_b):
        if op_code in self.op_table:
            self.op_table[op_code](operand_a, operand_b)
            num_operands = (op_code & 0b11000000) >> 6
            sets_pc = (op_code & 0b00010000) >> 4
            if not sets_pc:
                self.cpu.pc += num_operands + 1
        else:
            raise Exception(f"Unsupported operation: {op_code}")


class ALUOpDispatch(OpDispatch):
    def __init__(self, cpu):
        super().__init__(cpu)

        self.op_table = {
            0b10100000: self.ADD,
            0b10101000: self.AND,
            0b10100111: self.CMP,
            0b01100110: self.DEC,
            0b10100011: self.DIV,
            0b01100101: self.INC,
            0b10100100: self.MOD,
            0b10100010: self.MUL,
            0b01101001: self.NOT,
            0b10101010: self.OR,
            0b10101100: self.SHL,
            0b10101101: self.SHR,
            0b10100001: self.SUB,
            0b10101011: self.XOR
        }

    def ADD(self, a, b):
        self.reg[a] = (self.reg[a] + self.reg[b]) & 0xFF

    def AND(self, a, b):
        pass

    def CMP(self, a, b):
        pass

    def DEC(self, a, b):
        pass

    def DIV(self, a, b):
        pass

    def INC(self, a, b):
        pass

    def MOD(self, a, b):
        pass

    def MUL(self, a, b):
        self.reg[a] = (self.reg[a] * self.reg[b]) & 0xFF

    def NOT(self, a, b):
        pass

    def OR(self, a, b):
        pass

    def SHL(self, a, b):
        pass

    def SHR(self, a, b):
        pass

    def SUB(self, a, b):
        pass

    def XOR(self, a, b):
        pass


class CPUOpDispatch(OpDispatch):
    def __init__(self, cpu):
        super().__init__(cpu)

        self.op_table = {
            0b01010000: self.CALL,
            0b00000001: self.HLT,
            0b01010010: self.INT,
            0b00010011: self.IRET,
            0b01010101: self.JEQ,
            0b01011010: self.JGE,
            0b01010111: self.JGT,
            0b01011001: self.JLE,
            0b01011000: self.JLT,
            0b01010100: self.JMP,
            0b01010110: self.JNE,
            0b10000011: self.LD,
            0b10000010: self.LDI,
            0b00000000: self.NOP,
            0b01000110: self.POP,
            0b01001000: self.PRA,
            0b01000111: self.PRN,
            0b01000101: self.PUSH,
            0b00010001: self.RET,
            0b10000100: self.ST
        }

    def HLT(self, a, b):
        self.cpu.stop()

    def INT(self, a, b):
        pass

    def IRET(self, a, b):
        pass

    def JEQ(self, a, b):
        pass

    def JGE(self, a, b):
        pass

    def JGT(self, a, b):
        pass

    def JLE(self, a, b):
        pass

    def JLT(self, a, b):
        pass

    def JMP(self, a, b):
        pass

    def JNE(self, a, b):
        pass

    def LD(self, a, b):
        pass

    def LDI(self, a, b):
        self.reg[a] = b

    def NOP(self, a, b):
        pass

    def POP(self, a, b):
        self.reg[a] = self.cpu.ram_read(self.reg[7])
        self.reg[7] += 1

    def PRA(self, a, b):
        pass

    def PRN(self, a, b):
        print(self.reg[a])

    def PUSH(self, a, b):
        self.reg[7] -= 1
        sp = self.reg[7]
        val = self.reg[a]
        self.cpu.ram_write(sp, val)

    def CALL(self, a, b):
        subroutine_pc = self.reg[a]
        print('calling: ', a, subroutine_pc, self.cpu.pc + 2)
        self.reg[a] = self.cpu.pc + 2
        print('return_pc in call: ', self.reg[a])
        self.PUSH(a, b)
        self.reg[a] = subroutine_pc
        self.cpu.pc = subroutine_pc

    def RET(self, a, b):
        reg_0_original_val = self.reg[0]
        self.POP(0, b)
        return_pc = self.reg[0]
        self.reg[0] = reg_0_original_val
        print('return_pc in ret: ', return_pc)
        self.cpu.pc = return_pc

    def ST(self, a, b):
        pass


class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        # Local variable in #run
        #  self.IR = 0
        # Readme says I don't need these.
        #  self.MAR = 0
        #  self.MDR = 0
        self.fl = 0b00000000
        self.running = True
        self.cpu_op_dispatch = CPUOpDispatch(self)
        self.alu_op_dispatch = ALUOpDispatch(self)
        self.op_table = {}

    def stop(self):
        self.running = False

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, program_file_name):
        """Load a program into memory."""

        address = 0

        program = []

        with open(program_file_name) as f:
            lines = f.readlines()
            for line in lines:
                clean_line = line.split('#')[0].strip()
                if clean_line:
                    program.append(int(clean_line, 2))
                else:
                    # blank line or comment
                    pass

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        pass

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |" % (
                self.pc,
                #self.fl,
                #self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2)),
            end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            alu_op = (IR & 0b00100000) >> 5
            if alu_op:
                self.alu_op_dispatch.execute(IR, operand_a, operand_b)
            else:
                self.cpu_op_dispatch.execute(IR, operand_a, operand_b)
