import unittest

from src.byteDecoder import ByteDecoder


class ByteDecoderTest(unittest.TestCase):
    def test_first_digit(self):
        self.assertEqual(ByteDecoder(b'\x12\x34').digit_at(0), 0x1)

    def test_second_digit(self):
        self.assertEqual(ByteDecoder(b'\x12\x34').digit_at(1), 0x2)

    def test_third_digit(self):
        self.assertEqual(ByteDecoder(b'\x12\x34').digit_at(2), 0x3)

    def test_fourth_digit(self):
        self.assertEqual(ByteDecoder(b'\x12\x34').digit_at(3), 0x4)

    def test_two_digit_number_at_0(self):
        self.assertEqual(ByteDecoder(b'\x12\x34').get_number(0, 1), 0x12)

    def test_two_digit_number_at_1(self):
        self.assertEqual(ByteDecoder(b'\x12\x34').get_number(1, 2), 0x23)

    def test_two_digit_number_at_2(self):
        self.assertEqual(ByteDecoder(b'\x12\x34').get_number(2, 3), 0x34)


if __name__ == '__main__':
    unittest.main()
