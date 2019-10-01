
def stringToHex(stringInput):
  return ''.join(hex(ord(x))[2:] for x in stringInput) 


def getHexwords(msg):
    hexwords = []
    for i in range(0, len(msg), 8):
        msgBlock = msg[i:i+8]
        m = stringToHex(msgBlock)
        hexwords.append(m)

    last = hexwords[-1]
    hexwords[-1] += ''.join(['0'] * (16-len(last)))
    return hexwords

def stringToBits(string_input):
  string_output = bitarray.bitarray()
  string_output.frombytes(string_input.encode("utf-8"))
  return string_output.to01()

def leftshift(array, value):
  return array[value:] + array[:value]

def hexToBinary(hexstr):
  return str(bin(int(hexstr, 16)))[2:].rjust(64, '0')


def getBinWords(hexWords):
  binWords = []
  for message in hexWords:
    binWord = hexToBinary(message)
    binWords.append(binWord)
  return binWords


def xor(val1, val2):
  xoredBits = [] 
  for i in range(len(val1)):
    bit1 = int(val1[i])
    bit2 = int(val2[i])
    xorBit = int(bool(bit1) ^ bool(bit2))
    xoredBits.append(xorBit)
  return ''.join(map(str,xoredBits))

def binaryToDec(binNum):
  return int(binNum,2)


def getXORed(val1, val2):
    bin1 = hexToBinary(val1)
    bin2 = hexToBinary(val2)
    return xor(bin1,bin2)


def binToHex(val):
    return hex(int(val, 2))



if __name__ == "__main__":
    val1 = "b0906968c5ca5a552b2740439c942e27f9b8b9b8f5faa057b779093fcf4beb70"
    val2 = "b0987970e5e26a6d6b6f101bfcfc5e5f793029205552babdbbbf404b1c1c4e4f"
    print(binToHex((getXORed(val1,val2))))

    
    
    