import time

class CPU4Bit:
    def __init__(self):
        self.A = 0          # 4-bit register
        self.PC = 0         # program counter
        self.C = 0          # carry flag
        self.RAM = [0] * 4  # 4 instrukcje
        self.clock_hz = 1

    def load_program(self, program):
        self.RAM = program[:4]

    def step(self):
        instr = self.RAM[self.PC]
        opcode = (instr >> 4) & 0b11
        operand = instr & 0b1111

        if opcode == 0b00:      # NOP
            pass

        elif opcode == 0b01:    # LOAD A, imm
            self.A = operand

        elif opcode == 0b10:    # ADD A, imm
            result = self.A + operand
            self.C = 1 if result > 15 else 0
            self.A = result & 0b1111

        elif opcode == 0b11:    # XOR A, imm
            self.A ^= operand

        self.PC = (self.PC + 1) & 0b11

    def run(self, cycles=10):
        for _ in range(cycles):
            self.step()
            print(f"PC={self.PC} A={self.A} C={self.C}")
            time.sleep(1 / self.clock_hz)


if __name__ == "__main__":
    cpu = CPU4Bit()

    program = [
    0b00010010,  # LOAD A, 2
    0b00100010,  # ADD A, 2
    0b00000000,  # NOP
    0b00000000
]

    cpu.load_program(program)
    cpu.clock_hz = 2
    cpu.run(4)

    print("FINAL RESULT:", cpu.A, "CARRY:", cpu.C)
