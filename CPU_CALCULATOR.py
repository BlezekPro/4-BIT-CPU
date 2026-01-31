# Prosty "assembler" + emulator 4-bitowego CPU

class CPU4Bit:
    def __init__(self):
        self.A = 0
        self.C = 0
        self.PC = 0
        self.RAM = [0] * 4

    def load_program(self, program):
        self.RAM = program[:4]

    def step(self):
        instr = self.RAM[self.PC]
        opcode = (instr >> 4) & 0b11
        operand = instr & 0b1111

        if opcode == 0b01:      # LOAD
            self.A = operand

        elif opcode == 0b10:    # ADD
            result = self.A + operand
            self.C = 1 if result > 15 else 0
            self.A = result & 0b1111

        self.PC = (self.PC + 1) & 0b11


# === ASSEMBLER ===

def assemble(expr):
    expr = expr.replace(" ", "")

    if "+" not in expr:
        raise ValueError("Obsługuję tylko dodawanie, np. 2 + 2")

    a, b = expr.split("+")
    a = int(a)
    b = int(b)

    if not (0 <= a <= 15 and 0 <= b <= 15):
        raise ValueError("Liczby muszą być z zakresu 0–15")

    instr_load = (0b01 << 4) | a
    instr_add  = (0b10 << 4) | b

    return [
        instr_load,
        instr_add,
        0b00000000,
        0b00000000
    ]


# === MAIN ===

if __name__ == "__main__":
    expr = input("Wpisz działanie (np. 2 + 2): ")

    program = assemble(expr)

    print("\nKod maszynowy:")
    for i, instr in enumerate(program):
        print(f"{i}: {instr:08b}")

    cpu = CPU4Bit()
    cpu.load_program(program)

    for _ in range(4):
        cpu.step()

    print("\nWYNIK:")
    print("A =", cpu.A)
    print("CARRY =", cpu.C)
