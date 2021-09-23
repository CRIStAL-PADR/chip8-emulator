import unittest

from src.chip8interpreter import Chip8Interpreter


class Chip8InterpreterTest(unittest.TestCase):
    def test_index_default_value(self):
        interpreter = Chip8Interpreter(b'')
        self.assertEqual(interpreter.I, 0)

    def test_store_address_in_index(self):
        interpreter = Chip8Interpreter(b'\xA2\xB4')
        interpreter.step()
        self.assertEqual(interpreter.I, 0x2b4)

    def test_execute_one_instruction_of_two(self):
        # 0000: I := 0x17
        # 0002: I := 0x53
        interpreter = Chip8Interpreter(b'\xA0\x17\xA0\x53')
        interpreter.step()
        self.assertEqual(interpreter.I, 0x17)

    def test_execute_two_instructions(self):
        # 0000: I := 0x17
        # 0002: I := 0x53
        interpreter = Chip8Interpreter(b'\xA0\x17\xA0\x53')
        interpreter.step()
        interpreter.step()
        self.assertEqual(interpreter.I, 0x53)

    def test_execute_two_instructions_with_jump(self):
        # 0000: JUMP 0x4
        # 0002: I := 17
        # 0004: I := 53
        interpreter = Chip8Interpreter(b'\x10\x04\xA0\x17\xA0\x53')
        interpreter.step()
        interpreter.step()
        self.assertEqual(interpreter.I, 0x53)

    def test_register_out_of_bounds_raises_error(self):
        interpreter = Chip8Interpreter(b'')

        with self.assertRaises(IndexError) as error:
            interpreter.get_register(16)

    def test_register_out_of_negative_bounds_raises_error(self):
        interpreter = Chip8Interpreter(b'')

        with self.assertRaises(IndexError) as error:
            interpreter.get_register(-1)

    def test_default_registers(self):
        interpreter = Chip8Interpreter(b'')
        # Test registers between 0 and 15 (in hexa)
        for i in range(0, 0xf):
            self.assertEqual(interpreter.get_register(i), 0)
