from .utils import type2bit


class TLMBase:
    def __init__(self):
        self.octet_pos = 0
        self.bit_pos = 0
        self.bit_len = 0

    def update_pos(self, data=None, is_comp=False):
        data = self.data if data is None else data
        self.octet_pos += int((self.bit_pos + self.bit_len) / 8)
        self.bit_pos = (self.bit_pos + self.bit_len) % 8
        if is_comp:
            self.bit_len = data["bitlen"]
        else:
            self.bit_len = type2bit[data["type"]]


class SGCBase:
    def __init__(self):
        self.code = 0

    def update_code(self):
        if "code" in self.data and self.data["code"] != "":
            self.code = int(self.data["code"], 16)
        else:
            self.code += 1
