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

    def test_graphic_memory_initialization(self):
        interpreter = Chip8Interpreter(b'')
        self.assertEqual(interpreter.get_pixel(0, 0), 0)
        self.assertEqual(interpreter.get_pixel(63, 31), 0)

    def test_graphic_memory_put_pixel(self):
        interpreter = Chip8Interpreter(b'')
        interpreter.put_pixel(42, 17, 1)
        self.assertEqual(interpreter.get_pixel(42, 17), 1)

    def test_graphic_memory_out_of_bounds(self):
        interpreter = Chip8Interpreter(b'')

        with self.assertRaises(IndexError) as error:
            interpreter.get_pixel(64, 31)

        with self.assertRaises(IndexError) as error:
            interpreter.get_pixel(63, 32)

        with self.assertRaises(IndexError) as error:
            interpreter.get_pixel(-1, 17)

        with self.assertRaises(IndexError) as error:
            interpreter.get_pixel(17, -1)

    def test_execute_sprite(self):
        # 0000: sprite v0 v0 1 (I implicitly gives the sprite address)
        interpreter = Chip8Interpreter(b'\xD0\x01\x12')
        # Force the Index register to point to the byte 2
        # The byte 2 contains the sprite to draw
        interpreter.I = 2
        interpreter.step()

        # The drawn sprite should look like: 00010010
        # Each element is a pixel turned on
        self.assertPixelLine(interpreter, 0, 0, "00010010")

    def test_execute_two_tall_sprite(self):
        # 0000: sprite v0 v0 2 (I implicitly gives the sprite address)
        interpreter = Chip8Interpreter(b'\xD0\x02\x12\x34')
        # Force the Index register to point to the byte 2
        # The byte 2 contains the sprite to draw
        interpreter.I = 2
        interpreter.step()

        # The drawn sprite should look like:
        #   00010010
        #   00110100
        # Each element is a pixel turned on
        self.assertPixelLine(interpreter, 0, 0, "00010010")
        self.assertPixelLine(interpreter, 0, 1, "00110100")

    def assertPixelLine(self, interpreter, x, y, expected_pattern):
        got_pattern = ""
        for i in range(x, x + 8):
            got_pattern += str(interpreter.get_pixel(i, y))
        self.assertEqual(expected_pattern, got_pattern)
