S = [[7, 12, 14, 9, 2, 1, 5, 15, 11, 6, 13, 0, 4, 8, 10, 3],
    [4, 10, 1, 6, 8, 15, 7, 12, 3, 0, 14, 13, 5, 9, 11, 2],
    [2, 15, 12, 1, 5, 6, 10, 13, 14, 8, 3, 4, 0, 11, 9, 7],
    [15, 4, 5, 8, 9, 7, 2, 1, 10, 3, 0, 14, 6, 12, 13, 11]]

KEYBOX = [2,14,15,5,12,1,9,10,11,4,6,8,0,7,3,13]

WEIGHT_CHUNK_SIZE = 4

def binaryToDec(binNum):
  return int(binNum,2)


def leftshift(array, value):
    return array[value:] + array[:value]

def xor(val1, val2):
  xoredBits = [] 
  for i in range(len(val1)):
    bit1 = int(val1[i])
    bit2 = int(val2[i])
    xorBit = int(bool(bit1) ^ bool(bit2))
    xoredBits.append(xorBit)
  return ''.join(map(str,xoredBits))

def keyGen(key):
  '''
  Take the 80-bit key and extract leftmost 16 bits of current MK as RK0.
  
  For i<64, do the following update :
  1) MK << 13 
  2) i) [k0 k1 k2 k3] <- S[k0 k1 k2 k3]
     ii)[k64 k65 k66 k67] <- S[k64 k65 k66 k67]
     iii) [k76 k77 k78 k79] <- S[k76 k77 k78 k79]
  3) [k68 k69 k70 k71 k72 k73 k74 k75] <- [k68 k69 k70 k71 k72 k73 k74 k75] xor [i]2
  
  i = i+1
  
  '''

  subKeys = []
  key = list(key)
  print(key)
  for i in range(32):
    #append the ith key at the start of the loop. 
    subKeys.append(''.join(key[:16]))
    
    key = leftshift(key,13)
    #extract the elements that are gonna be S-Boxed
    
    keyBlockA = list(str(format(KEYBOX[binaryToDec(''.join(key[:4]))],"b").zfill(4))) #1st
    keyBlockB = list(str(format(KEYBOX[binaryToDec(''.join(key[64:68]))],"b").zfill(4))) #3rd
    keyBlockC = list(str(format(KEYBOX[binaryToDec(''.join(key[76:80]))],"b").zfill(4))) #5th

    #Get the remainder of the key 
    keyBlockD = key[4:64] #2nd
    keyBlockE = key[68:76] #4th

    #assemble the key again 
    key = keyBlockA+keyBlockD+keyBlockB+keyBlockE+keyBlockC

    # #idek what theyre doing at this point
    keyBlockD = key[68:76]
    iBin = list(str(format(i,"b").zfill(8)))
    keyBlockF = list(xor(keyBlockD,iBin))
    
    keyBlockG = key[:68]
    keyBlockH = key[76:80]
    key = keyBlockG+keyBlockF+keyBlockH

    print("The subkey for round {} is {}".format(str(i), subKeys[i]))
    
def test():
    print(keyGen("00000000001111111111000000000011111111110000000000111111111100000000001111111111"))

if __name__ == "__main__":
    test()
