import unittest

from src.chip8disassembler import Chip8Disassembler


def disassemble(bytes_to_disassemble):
    return Chip8Disassembler().disassemble(bytes_to_disassemble)


class Chip8DecompilerTest(unittest.TestCase):
    def test_store_address_in_index(self):
        self.assertEqual(disassemble(b'\xA2\xB4'), 'I := 0x2b4')

    def test_jump(self):
        self.assertEqual(disassemble(b'\x12\xB4'), 'JUMP 0x2b4')

    def test_store_address_in_index2(self):
        self.assertEqual(disassemble(b'\xA1\x23'), 'I := 0x123')

    def test_call(self):
        self.assertEqual(disassemble(b'\x23\xE6'), 'CALL 0x3e6')

    def test_call2(self):
        self.assertEqual(disassemble(b'\x21\x23'), 'CALL 0x123')

    def test_accumulator_v0_plus_one(self):
        self.assertEqual(disassemble(b'\x70\x01'), 'V0 := V0 + 0x01')

    def test_accumulator_v0(self):
        self.assertEqual(disassemble(b'\x70\x23'), 'V0 := V0 + 0x23')

    def test_accumulator_va(self):
        self.assertEqual(disassemble(b'\x7A\x23'), 'VA := VA + 0x23')

    def test_invalid_instruction(self):
        self.assertEqual(disassemble(b'\xF0\x00'), 'Undefined (0xF000)')

    def test_copy_1_to_2(self):
        self.assertEqual(disassemble(b'\x82\x10'), 'V2 := V1')

    def test_undefined_8_family_instruction(self):
        self.assertEqual(disassemble(b'\x80\x08'), 'Undefined (0x8008)')

    def test_disassemble_stream(self):
        self.assertEqual(self.disassemble_stream(
            b'\xA2\xB4\x23\xE6\x70\x01', 3),
            "I := 0x2b4\n"
            "CALL 0x3e6\n"
            "V0 := V0 + 0x01\n")

    def test_disassemble_stream_starting_at_2(self):
        self.assertEqual(self.disassemble_stream(
            b'\xA2\xB4\x23\xE6\x70\x01', 2, 2),
            "CALL 0x3e6\n"
            "V0 := V0 + 0x01\n")

    def test_disassemble_more_than_available(self):
        self.assertEqual(self.disassemble_stream(
            b'', 1),
            "EOF\n")

    def test_something(self):
        bytes_to_disassemble = b'\xA2\xB4\x23\xE6\x22\xB6\x70\x01\xD0\x11\x30\x25\x12\x06\x71\xFF'
        self.assertEqual(bytes_to_disassemble[0], 162)

    @staticmethod
    def disassemble_stream(bytes_to_disassemble, number_of_instruction, position=0):
        return Chip8Disassembler().disassemble_stream(bytes_to_disassemble, number_of_instruction, position)


if __name__ == '__main__':
    unittest.main()
