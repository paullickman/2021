import math

class Packet:
    def __init__(self, file=None, transmission=None):
        if file:
            transmission = open('16/' + file).read().strip()
        self.transmission = ''.join([bin(int(t, 16))[2:].zfill(4) for t in transmission])
        self.pointer = 0
        self.versionSum = 0
        self.result = self.parse()

    def parse(self):
        # Check for trailing zeros
        if all(t == '0' for t in self.transmission[self.pointer:]):
            return None

        # Version number
        version = int(self.transmission[self.pointer:self.pointer+3], 2)
        self.versionSum += version
        self.pointer += 3

        # Type ID
        typeID = int(self.transmission[self.pointer:self.pointer+3], 2)
        self.pointer += 3

        if typeID == 4:
            # Literal value
            value = self.transmission[self.pointer+1:self.pointer+5]
            self.pointer += 5
            while self.transmission[self.pointer-5] == '1':
                value += self.transmission[self.pointer+1:self.pointer+5]
                self.pointer += 5
            value = int(value, 2)
            #print('Literal =', value)
            return value
        else:
            # Operator

            values = []

            # Length type ID
            lengthTypeID = int(self.transmission[self.pointer])
            self.pointer += 1

            if lengthTypeID == 0:
                totalLength = int(self.transmission[self.pointer:self.pointer+15],2)
                self.pointer += 15

                end = self.pointer + totalLength
                while self.pointer < end:
                    values.append(self.parse())
            else:
                numPackets = int(self.transmission[self.pointer:self.pointer+11],2)
                self.pointer += 11

                for _ in range(numPackets):
                    values.append(self.parse())

            match typeID:
                case 0: # Sum
                    return sum(values)
                case 1: # Product
                    return math.prod(values)
                case 2: # Minimum
                    return min(values)
                case 3: # Maximum
                    return max(values)
                case 5: # Greater than
                    return 1 if values[0]>values[1] else 0
                case 6: # Less than
                    return 1 if values[0]<values[1] else 0
                case 7: # Equal
                    return 1 if values[0]==values[1] else 0
                case _: # Unknown
                    print('Unknown operator id', typeID)
 
# Part 1

p = Packet(transmission='8A004A801A8002F478')
assert p.versionSum == 16

p = Packet(transmission='620080001611562C8802118E34')
assert p.versionSum == 12

p = Packet(transmission='C0015000016115A2E0802F182340')
assert p.versionSum == 23

p = Packet(transmission='A0016C880162017C3686B18A3D4780')
assert p.versionSum == 31

p = Packet(file='input.txt')
print(p.versionSum)

# Part 2
p = Packet(transmission='C200B40A82')
assert p.result == 3

p = Packet(transmission='04005AC33890')
assert p.result == 54

p = Packet(transmission='880086C3E88112')
assert p.result == 7

p = Packet(transmission='CE00C43D881120')
assert p.result == 9

p = Packet(transmission='D8005AC2A8F0')
assert p.result == 1

p = Packet(transmission='F600BC2D8F')
assert p.result == 0

p = Packet(transmission='9C005AC2F8F0')
assert p.result == 0

p = Packet(transmission='9C0141080250320F1802104A08')
assert p.result == 1

p = Packet(file='input.txt')
print(p.result)
