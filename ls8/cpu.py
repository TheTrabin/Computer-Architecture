"""CPU functionality."""

import sys

# Other Commands
# NOP = 0b00000000 # Nothing
LDI = 0b10000010 # Load Data Immediately. Requires Registar as second, Value in first
PRN = 0b01000111 # Print Value
HLT = 0b00000001
LD = 0b10000011
ST = 0b10000100
PUSH = 0b01000101
POP = 0b01000110
PRA = 0b01001000

# ALU Commands
ADD = 0b10100000 # Addition
SUB = 0b10100001 # Subtraction
MUL = 0b10100010 # Multiplication
DIV = 0b10100011 # Division
MOD = 0b10100100 # Modulo
CMP = 0b10100111 # Comparable

CALL = 0b01010000
RET = 0b00010001
JEQ = 0b01010101
JMP = 0b01010100
JNE = 0b01010110

SP = 7 # pointer

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # self.running = True
        self.halted = False
        self.pc = 0
        self.ir = 0
        self.fl = 0
        self.mar = 0
        self.mdr = 0

        self.reg = [0] * 8
        # self.registers = [0] * 8
        self.reg[7] = 0xF4
        # self.registers[7] = 0xF4

        self.ram = [0] * 256
        
        self.less = 0
        self.greater = 0
        self.equal = 0

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        program = []
      
        with open(filename) as my_file:
            for line in my_file:
                comment_split = line.split("#")
                maybe_binary_number = comment_split[0]
                try:
                    x = int(maybe_binary_number, 2)
                    self.ram_write(x, address)
                    address += 1
                except:
                    continue
      
        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.less = 1
            if self.reg[reg_a] > self.reg[reg_b]:
                self.greater = 1
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.equal = 1
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

    def num_of_ops(self, instruction):
        return ((instruction >> 6) & 0b11) + 1

    def run(self):
        """Run the CPU."""
        # self.trace()

        while not self.halted:
            # ir = self.ram_read(self.pc)
            instruction_to_execute = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(instruction_to_execute, operand_a, operand_b)

    def execute_instruction(self, instruction, operand_a, operand_b):
        if instruction == HLT:
            print("stopping")
            self.halted = True
            
        if instruction == PRN:
            print(self.reg[operand_a])
            self.pc += 2

        elif instruction == LDI:
            self.reg[operand_a] = operand_b
            self.pc += 3

        elif instruction == MUL:
            self.alu(instruction, operand_a, operand_b)
            self.pc += 3

        elif instruction == ADD:
            self.alu(instruction, operand_a, operand_b)
            self.pc += 3

        elif instruction == SUB:
            self.alu("SUB", operand_a, operand_b)
            self.pc += 3

        elif instruction == DIV:
            self.alu("DIV", operand_a, operand_b)
            self.pc += 3

        elif instruction == POP:
           self.reg[operand_a] = self.ram[self.reg[SP]]
           self.reg[SP] += 1
           self.pc += 2

        elif instruction == PUSH:
            self.reg[SP] -= 1
            self.ram[self.reg[SP]] = self.reg[operand_a]
            self.pc += 2

        elif instruction == CALL:
            self.reg[SP] -= 1
            self.ram[self.reg[SP]] = self.reg[operand_a]
            self.pc = self.reg[operand_a]

        elif instruction == RET:
            self.pc = self.ram_read[self.reg[SP]]
            self.reg[self.reg[SP]] += 1

        elif instruction == JMP:
            self.pc = self.reg[operand_a]

        elif instruction == JEQ:
            if self.equal == 1:
                self.pc = self.reg[operand_a]

            else:
                self.pc += 2

        elif instruction == JNE:
            if self.equal == 0:
                self.pc = self.reg[operand_a]
            else:
                self.pc += 2

        else:
            print(f"idk what to do. {instruction}")
            sys.exit(1)
    
    