"""CPU functionality."""

import sys

# Other Commands
# NOP = 0b00000000 # Nothing
LDI = 0b10000010 # Load Data Immediately. Requires Registar as second, Value in first
PRN = 0b01000111 # Print Value
HLT = 0b00000001
# LD = 0b10000011
# ST = 0b10000100
# PUSH = 0b01000101
# POP = 0b01000110
# PRA = 0b01001000

# ALU Commands
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ir = 0
        self.running = True
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # 0b is calling the action, meaning "this is code for 0-level base"
        # 8 bit operator is the code for the particular program
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000, # R0 - Register 0
            0b00001000, # Value
            0b01000111, # PRN R0 - Print Registar 0
            0b00000000, # R0 - Register 0
            0b00000001, # HLT
        ]

        # position in program. Program is 'memory'
        # if this, then that

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

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.trace()

        while self.running == True:
            comm = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]


            if comm == HLT:
                self.running = False
                self.pc += 1
            elif comm == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif comm == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            else:
                print(f'Command not found. Please try again.')