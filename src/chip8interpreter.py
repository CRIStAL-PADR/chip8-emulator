from src.byteDecoder import ByteDecoder


class Chip8Interpreter:

    def __init__(self, program):
        super().__init__()
        self.I = 0
        self.PC = 0
        self.program = program
        self.registers = [0] * 16
        self.graphic_memory = [0] * (64 * 32)

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
        elif opcode == 0xD:
            decoder = ByteDecoder(instruction_bytes)
            vx = decoder.digit_at(1)
            vy = decoder.digit_at(2)
            height = decoder.digit_at(3)
            self.draw_sprite(self.get_register(vx), self.get_register(vy), height, self.I)
        else:
            raise Exception("Undefined instruction")

    """
    Get the value of the register @register_id
    Only register ids between 0 and 15 are allowed
    Registers out of those bounds raise an IndexError
    """
    def get_register(self, register_id):
        if register_id < 0:
            raise IndexError(register_id)
        return self.registers[register_id]

    def get_pixel(self, x, y):
        if x < 0:
            raise IndexError(x)
        if y < 0:
            raise IndexError(y)
        return self.graphic_memory[y * 64 + x]

    def put_pixel(self, x, y, pixel_value):
        self.graphic_memory[y * 64 + x] = pixel_value

    def draw_sprite(self, x, y, height, sprite_address):
        for h in range(0, height):
            sprite_byte = self.program[sprite_address + h]
            for i in range(1, 8):
                pixel_value = (sprite_byte >> (8-i)) & 0x1
                self.put_pixel(x + i - 1, y + h, pixel_value)
