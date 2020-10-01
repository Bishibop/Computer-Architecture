"""CPU functionality."""

import sys


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
        self.ops = {
            0b10100000: "ADD",
            0b10101000: "AND",
            0b01010000: "CALL",
            0b10100111: "CMP",
            0b01100110: "DEC",
            0b10100011: "DIV",
            0b00000001: "HLT",
            0b01100101: "INC",
            0b01010010: "INT",
            0b00010011: "IRET",
            0b01010101: "JEQ",
            0b01011010: "JGE",
            0b01010111: "JGT",
            0b01011001: "JLE",
            0b01011000: "JLT",
            0b01010100: "JMP",
            0b01010110: "JNE",
            0b10000011: "LD",
            0b10000010: "LDI",
            0b10100100: "MOD",
            0b10100010: "MUL",
            0b00000000: "NOP",
            0b01101001: "NOT",
            0b10101010: "OR",
            0b01000110: "POP",
            0b01001000: "PRA",
            0b01000111: "PRN",
            0b01000101: "PUSH",
            0b00010001: "RET",
            0b10101100: "SHL",
            0b10101101: "SHR",
            0b10000100: "ST",
            0b10100001: "SUB",
            0b10101011: "XOR",
        }

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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
        running = True
        while running:
            IR = self.ram_read(self.pc)
            command = self.ops[IR]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if command == "HLT":
                running = False
            elif command == "LDI":
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif command == "PRN":
                print(self.reg[operand_a])
                self.pc += 2
            else:
                # Is this actually what I'm supposed to do on an uncognized OP?
                print("Unrecognized OP code. Exiting...")
                sys.exit(1)
