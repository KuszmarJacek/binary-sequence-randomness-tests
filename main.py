# https://en.wikipedia.org/wiki/Shrinking_generator 
class ShrinkingGenerator:
    def __init__(self, feedbackPoly1, init1, feedbackPoly2, init2):
        self.x1 = LFSR(feedbackPoly1, init1)
        self.x2 = LFSR(feedbackPoly2, init2)

    def next(self):    
        b1 = self.x1.next()
        b2 = self.x2.next()

        while b1 == 0:
            b1 = self.x1.next()
            b2 = self.x2.next()

        return b2
            
    def get_n_bits(self, n):
        value = ""
        for i in range(n):
            value = value + str(self.next())
        return value
           
# https://en.wikipedia.org/wiki/Correlation_attack
class GeffesGenerator:
    def __init__(self, feedbackPoly1, init1, feedbackPoly2, init2, feedbackPoly3, init3):
        self.x1 = LFSR(feedbackPoly1, init1)
        self.x2 = LFSR(feedbackPoly2, init2)
        self.x3 = LFSR(feedbackPoly3, init3)

    def get_n_bit(self, n):
        value = ""
        for i in range(n):
            value = value + str(self.next())
        return value
        
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
    def __init__(self, feedbackPoly1, init1, feedbackPoly2, init2, feedbackPoly3, init3):
        self.x1 = LFSR(feedbackPoly1, init1)
        self.x2 = LFSR(feedbackPoly2, init2)
        self.x3 = LFSR(feedbackPoly3, init3)
        self.b1 = self.x1.next() & 1
        self.b2 = self.x2.next() & 1
        self.b3 = self.x3.next() & 1
    
    def next(self):
        self.b1 = self.x1.next() & 1
        if (self.b1 == 1):
            self.b2 = self.x2.next() & 1
        else:
            self.b3 = self.x3.next() & 1
        
        return self.b2 ^ self.b3
    
    def get_n_bit(self, n):
        value = ""
        for i in range(n):
            value = value + str(self.next())
        return value

class LFSR:
    def __init__(self, feedbackPoly, initialRegister):
        self.register = initialRegister
        self.feedbackPoly = feedbackPoly

    def next(self):
        res = 1
        # print(self.register)
        for k in self.feedbackPoly:
            res ^= self.register[k]
        poppedRegister = self.register.pop()
        self.register.insert(0, poppedRegister)
        self.register[0] = res
        # print(self.register)
        # print(res)
        return res

    def get_n_bits(self, n):
        for i in range(n):
            print(self.register)
            print(self.next())

def pokerTest(stream):
    counters = [0] * 16

    for i in range(5000):
        pack = int(stream[i * 4 : i * 4 + 4], 2)
        counters[pack] += 1

    sum = 0
    for v in counters:
        sum += (v * v)
    
    poker = 16 / 5000 * sum - 5000

    
    if poker > 2.16 and poker < 46.17:
        print("Positive poker test result: " + str(poker))
    else:
        print("Negative poker test result: " + str(poker))

def longRunsTest(stream):
    sameCnt = 0
    lastChar = ''
    positive = True

    for i in range(len(stream)):
        if stream[i] == lastChar:
            sameCnt = sameCnt + 1
        else:
            lastChar = stream[i]
            sameCnt = 1

        if sameCnt > 26:
            positive = False
            break

    if positive:
        print("Positive long runs test")
    else:
        print("Negative long runs test")

def runsTest(stream):
    sameCnt = 0
    lastChar = ''
    counters = [0] * 6

    for i in range(len(stream)):
        if stream[i] == lastChar:
            sameCnt = sameCnt + 1
        else:
            lastChar = stream[i]
            if sameCnt <= 6 and sameCnt > 0:
                counters[sameCnt - 1] = counters[sameCnt - 1] + 1
            else:
                counters[5] = counters[5] + 1
            sameCnt = 1
    
    if sameCnt <= 6:
        counters[sameCnt - 1] = counters[sameCnt - 1] + 1
    else:
        counters[5] = counters[5] + 1

    if\
        counters[0] >= 2315 and counters[0] <= 2685 or\
        counters[1] >= 1114 and counters[1] <= 1386 or\
        counters[2] >= 527 and counters[2] <= 723 or\
        counters[3] >= 240 and counters[3] <= 384 or\
        counters[4] >= 103 and counters[4] <= 209 or\
        counters[5] >= 103 and counters[5] <= 2685:
        print("Negative runs test")
    else:
        print("Positive runs test")
     

if __name__ == "__main__":
    initialRegister = [1, 0, 1, 1, 1, 0, 1, 0]
    reg = LFSR([0, 1, 2], initialRegister)
    bits = []
    bits.append(reg.next())
    bits.append(reg.next())
    bits.append(reg.next())
    print("Trzy bity z LFSR:      " + str(bits))

    geffeGenerator = GeffesGenerator([0, 1, 2], [1, 0, 1, 1, 1, 0, 1, 0], [2, 3, 1], [1, 1, 1, 1, 1, 1, 1, 0], [3, 4, 5], [1, 0, 0, 1, 1, 0, 1, 1])
    geffeBits = geffeGenerator.get_n_bit(20000)
    print("Generator geffe:       " + geffeGenerator.get_n_bit(100))

    stopAndGoGenerator = StopAndGoGenerator([0, 1, 2], [1, 0, 1, 1, 1, 0, 1, 0], [2, 3, 1], [1, 1, 1, 1, 1, 1, 1, 0], [3, 4, 5], [1, 0, 0, 1, 1, 0, 1, 1])
    stopAndGoBits = stopAndGoGenerator.get_n_bit(20000)
    print("Generator stop and go: " + stopAndGoGenerator.get_n_bit(100))

    shrinkingGenerator = ShrinkingGenerator([0, 1, 2], [1, 0, 1, 1, 1, 0, 1, 0], [2, 3, 1], [1, 1, 1, 1, 1, 1, 1, 0])
    shrinkingBits = shrinkingGenerator.get_n_bits(20000)
    print("Shrinking generator:   " + shrinkingGenerator.get_n_bits(100))

    print("Test results for geffe")
    pokerTest(geffeBits)
    longRunsTest(geffeBits)
    runsTest(geffeBits)

    print("Test results for stop and go")
    pokerTest(stopAndGoBits)
    longRunsTest(stopAndGoBits)
    runsTest(stopAndGoBits)

    print("Test results for shrinking")
    pokerTest(shrinkingBits)
    longRunsTest(shrinkingBits)
    runsTest(shrinkingBits)



            