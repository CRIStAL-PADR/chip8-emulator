from src.byteDecoder import ByteDecoder


class Chip8Disassembler:
    # noinspection PyMethodMayBeStatic
    def disassemble(self, bytes_to_disassemble):
        decoder = ByteDecoder(bytes_to_disassemble)
        opcode = decoder.digit_at(0)
        if opcode == 0x1:
            return 'JUMP ' + hex(decoder.get_number(1, 3))
        elif opcode == 0x2:
            return 'CALL ' + hex(decoder.get_number(1, 3))
        elif opcode == 0x7:
            register_number = decoder.digit_at(1)
            return 'V{0:X} := V{0:X} + 0x{1:02X}'.format(register_number, decoder.get_number(2, 3))
        elif opcode == 0x8:
            suffix = decoder.digit_at(3)
            if suffix == 0:
                x = decoder.digit_at(1)
                y = decoder.digit_at(2)
                return f'V{x:X} := V{y:X}'
        elif opcode == 0xA:
            return f'I := {hex(decoder.get_number(1, 3))}'
        elif opcode == 0xD:
            return f'sprite V{decoder.digit_at(1)} V{decoder.digit_at(2)} {hex(decoder.digit_at(3))}'
        return f'Undefined (0x{decoder.get_number(0, 3):04X})'

    def disassemble_stream(self, memory, number_of_instruction, initial_position):
        disassembled_string = ''
        final_position = initial_position + (number_of_instruction * 2)
        for i in range(initial_position, final_position, 2):
            instruction_bytes = memory[i:i + 2]

            # If we are after the end, the slice operator will give us an empty array
            if len(instruction_bytes) == 0:
                disassembled_string += "EOF\n"
                return disassembled_string

            disassembled_instruction = self.disassemble(instruction_bytes)
            disassembled_string += disassembled_instruction + '\n'
        return disassembled_string


if __name__ == '__main__':
    with open('/Users/guille/Downloads/CHIP8/GAMES/TETRIS', 'rb') as file:
        print(Chip8Disassembler().disassemble_stream(file.read(), 10, 0))
