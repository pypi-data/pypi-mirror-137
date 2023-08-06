import random
from ranstring import gen
gen.init(l)

char = [char for char in "abcdefghijklmnopqrstuvwxyz"]
num = [char for char in "123456789"]
class init():
    def __init__(self, len=4, chars=True, nums=False):
        self.len = len
        self.c = chars
        self.n = nums
    def gen(self):
        if self.c and not self.n:
            i = 0
            s = ""
            while i < self.len:
                s = s+random.choice(char)
                i = i + 1
            return s
        if not self.c and self.n:
            i = 0
            s = ""
            while i < self.len:
                s = s+random.choice(num)
                i = i + 1
            return s
        if self.c and self.n:
            i = 0
            s = ""
            while i < self.len:
                if random.choice([True, False]):
                    s = s+random.choice(num)
                else:
                    s = s+random.choice(char)
                i = i + 1
            return s
