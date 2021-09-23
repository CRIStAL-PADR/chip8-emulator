class Chip8Interpreter:

    def __init__(self, program):
        super().__init__()
        self.I = 0
        self.PC = 0
        self.program = program

    def step(self):
        self.execute(self.program[self.PC: self.PC + 2])

    def execute(self, instruction_bytes):
        first_byte = instruction_bytes[0]
        second_byte = instruction_bytes[1]
        opcode = first_byte >> 4
        if opcode == 0xA:
            N1 = first_byte & 0x0F
            value_to_assign = (N1 << 1 * 8) + second_byte
            self.I = value_to_assign
            self.PC += 2
        elif opcode == 0x1:
            N1 = first_byte & 0x0F
            jump_target = (N1 << 1 * 8) + second_byte
            self.PC = jump_target
        else:
            raise Exception("Undefined instruction")