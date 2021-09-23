class ByteDecoder:
    def __init__(self, bytes_to_decode):
        self.bytes = bytes_to_decode

    def digit_at(self, i):
        if i == 0:
            return self.bytes[0] >> 4
        elif i == 1:
            return self.bytes[0] & 0xF
        elif i == 2:
            return self.bytes[1] >> 4
        else:
            return self.bytes[1] & 0xF

    def get_number(self, first_index, last_index):
        result = 0
        for i in range(first_index, last_index + 1):
            result = (result * 16) + self.digit_at(i)
        return result
