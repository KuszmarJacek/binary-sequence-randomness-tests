# https://en.wikipedia.org/wiki/Xorshift
class XORShiftLFSR32:
    def __init__(self, seed):
        self.state = seed
        
    def next(self):
        self.state ^= self.state << 13
        self.state ^= self.state >> 17
        self.state ^= self.state << 5
        return self.state & 0xFFFFFFFF
    
class XORShiftLFSR64:
    def __init__(self, seed):
        self.state = seed
        
    def next(self):
        self.state ^= self.state << 13
        self.state ^= self.state >> 7
        self.state ^= self.state << 17
        return self.state & 0xFFFFFFFFFFFFFFFF

# https://en.wikipedia.org/wiki/Shrinking_generator
# https://github.com/mfukar/lfsr/blob/master/lfsr.py
class GLFSR:
    def __init__(self, polynom, initial_value):
        self.polynom = polynom | 1
        self.data = initial_value
        tmp = polynom
        self.mask = 1

        while tmp != 0:
            if tmp & self.mask != 0:
                tmp ^= self.mask

            if tmp == 0:
                break

            self.mask <<= 1

    def next_bit(self):
        self.data <<= 1

        if self.data & self.mask != 0:
            self.data ^= self.polynom
            return 1
        else:
            return 0

    def get_n_bit(self, n):
        value = 0
        for i in range(n):
            value = (value << 1) | self.next_bit()
        return bin(value)

# https://en.wikipedia.org/wiki/Shrinking_generator 
class SPRNG:
    def __init__(self, polynom_d, init_value_d, polynom_c, init_value_c):
        self.glfsr_d = GLFSR(polynom_d, init_value_d)
        self.glfsr_c = GLFSR(polynom_c, init_value_c)

    def next_bit(self):
        bit = 0
        bitpos = 1

        while True:
            bit_d = self.glfsr_d.next_bit()
            bit_c = self.glfsr_c.next_bit()

            if bit_c != 0:
                bit_r = bit_d
                bit |= bit_r << bitpos

                bitpos -= 1

                if bitpos < 0:
                    break

        return bit
            
    def get_n_bits(self, n):
        value = 0
        for i in range(n):
            value = (value << 1) | self.next_bit()
        return bin(value)
            
# https://en.wikipedia.org/wiki/Correlation_attack
class GeffesGenerator:
    def __init__(self, key1, key2, key3):
        self.x1 = XORShiftLFSR32(key1)
        self.x2 = XORShiftLFSR32(key2)
        self.x3 = XORShiftLFSR32(key3)

    def get_n_bit(self, n):
        value = 0
        for i in range(n):
            value = (value << 1) | self.next()
        return bin(value)
        
    # from lecture
    def next(self):
        b1 = self.x1.next() & 1
        b2 = self.x2.next() & 1
        b3 = self.x3.next() & 1
        # F(x1, x2, x3) = (x1 AND x2) XOR (!x2 AND x3)
        return (b1 & b2) ^ ((not b2) & b3)
    
    def next_wiki(self):
        b1 = self.x1.next() & 1
        b2 = self.x2.next() & 1
        b3 = self.x3.next() & 1
        # F(x1, x2, x3) = (x1 AND x2) XOR (!x1 AND x3)
        return (b1 & b2) ^ ((not b2) & b3)
    
class StopAndGoGenerator():
    def __init__(self, key1, key2, key3):
        self.x1 = XORShiftLFSR64(key1)
        self.x2 = XORShiftLFSR64(key2)
        self.x3 = XORShiftLFSR64(key3)
        self.b1 = self.x1.next() & 1
        self.b2 = self.x2.next() & 1
        self.b3 = self.x3.next() & 1
    
    def next(self):
        self.b1 = self.x1.next() >> 1
        if (self.b1 == 1):
            self.b2 = self.x2.next() >> 1
        else:
            self.b3 = self.x3.next() >> 1
        
        return self.b2 ^ self.b3
    
    def get_n_bit(self, n):
        value = 0
        for i in range(n):
            value = (value << 1) | self.next()
        return bin(value)



if __name__ == "__main__":
    lfsr = XORShiftLFSR32(123456)
    print(lfsr.next())
    generator = GeffesGenerator(123, 456, 789)
    print(generator.get_n_bit(10))


    sprng = SPRNG(0b11001, 0b101, 0b10011, 0b1100)
    print(sprng.get_n_bits(10))

    stopAndGoGenerator = StopAndGoGenerator(123, 456, 789)
    print(stopAndGoGenerator.get_n_bit(10))
            