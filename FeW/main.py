'''

Implementation of FeW 

Encrypts 64-bit blocks using 80/128 bit keys and produces 64 bit ciphertext.
Uses a Feistal-M structure where M=4 in this case.

'''

import os
import bitarray
import binascii


############################################ START OF CONSTANTS  #########################################

'''
S-Boxes as copied from Hummingbird-2

For the use of the S-Box, do the following: 

                     A     B      C      D
Let the input be : 0111 | 0110 | 0000 | 0001

Do the following: 
R1 = S0(A) = S0[7] = 15 = 1111
R2 = S1(B) = S1[6] = 7 = 0111
R3 = S2(C) = S2[0] =  2 = 0010
R4 = S3(D) = S3[1] = 4 = 0100


Therefore the output is 1111|0111|0010|0100

'''

S = [[7, 12, 14, 9, 2, 1, 5, 15, 11, 6, 13, 0, 4, 8, 10, 3],
    [4, 10, 1, 6, 8, 15, 7, 12, 3, 0, 14, 13, 5, 9, 11, 2],
    [2, 15, 12, 1, 5, 6, 10, 13, 14, 8, 3, 4, 0, 11, 9, 7],
    [15, 4, 5, 8, 9, 7, 2, 1, 10, 3, 0, 14, 6, 12, 13, 11]]

KEYBOX = [2,14,15,5,12,1,9,10,11,4,6,8,0,7,3,13]

NUM_ROUNDS = 32
ROUND_CHUNK_SIZE = 8
WEIGHT_CHUNK_SIZE = 4

########################################   END OF CONSTANTS   ##############################################



############################################ GENERIC FUNCTIONS   #########################################

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


################################### END OF GENERIC FUNCTIONS   #################################

########################### ENCRYPTION BEGINS HERE ##########################################

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
  
  for i in range(64):
    #append the ith key at the start of the loop.
  
    subKeys.append(''.join(key[:16]))
    key = leftshift(key,13) 
    
    for j in range(16):
      key.append('0')
    j = 0
    #extract the elements that are gonna be S-Boxed
    keyBlockA = list(str(format(KEYBOX[binaryToDec(''.join(key[:4]))],"b").zfill(4))) #1st
    keyBlockB = list(str(format(KEYBOX[binaryToDec(''.join(key[64:68:1]))],"b").zfill(4))) #3rd
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

  keys = []
  for i in range(int(len(subKeys)/2)):
    keys.append(subKeys[2*i]+subKeys[2*i+1])
    print("The {}th key is {}".format(i, keys[i]))
  return keys

def weightFunc1(A):
  '''Takes in A and gives S-Boxed answer with a bunch of specified left shifts'''
  bitBlock = [A[i:i+WEIGHT_CHUNK_SIZE] for i in range(0, len(A), WEIGHT_CHUNK_SIZE)]
  U0 = [] 
  for i in range(4):
    U0.append(str(format(S[i][binaryToDec(bitBlock[i])],"b")).zfill(4))
  U0 = ''.join(U0)

  UShift = []
  UShift.append(U0)
  UShift.append(leftshift(U0,1))
  UShift.append(leftshift(U0,5))
  UShift.append(leftshift(U0,9))
  UShift.append(leftshift(U0,12))
  
  UStrings = []
  for i in range(5):
    UStrings.append(''.join(UShift[i]))
  
  return xor(xor(xor(xor(UStrings[0],UStrings[1]),UStrings[2]),UStrings[3]),UStrings[4])


def weightFunc2(B):
  '''Takes in B and gives S-Boxed answer with a bunch of specified left shifts'''
  bitBlock = [B[i:i+WEIGHT_CHUNK_SIZE] for i in range(0, len(B), WEIGHT_CHUNK_SIZE)]
  U0 = [] 
  for i in range(4):
    U0.append(str(format(S[i][binaryToDec(bitBlock[i])],"b")).zfill(4))
  U0 = ''.join(U0)

  UShift = []
  UShift.append(U0)
  UShift.append(leftshift(U0,4))
  UShift.append(leftshift(U0,7))
  UShift.append(leftshift(U0,11))
  UShift.append(leftshift(U0,15))
  
  UStrings = []
  for i in range(5):
    UStrings.append(''.join(UShift[i]))
  
  return xor(xor(xor(xor(UStrings[0],UStrings[1]),UStrings[2]),UStrings[3]),UStrings[4])
  

def roundFunction(Xi, Ki):
  # XOR Xi and Ki 
  # Split the output into 4 8-bit blocks - C, D, E, F
  # Concatanate C&F to produce A and E&D to produce B 
  # Run A through WF1 and B through WF2 to produce Y. 
  #return Y 
  # print("Xi is {} and the length is {}".format(Xi, len(Xi)))
  # print("Ki is {} and the length is {}".format(Ki, len(Ki)))
  XiRi = xor(Xi, Ki)
  bitBlock = [XiRi[i:i+ROUND_CHUNK_SIZE] for i in range(0, len(XiRi), ROUND_CHUNK_SIZE)]
  A = bitBlock[0]+bitBlock[3]
  B = bitBlock[2] + bitBlock[1]
  return weightFunc1(A) + weightFunc2(B)

def messageEncryption(message, subkeys):
  tempMsg = message
  print("The whole message is : {}".format(tempMsg))
  print("The split message is {} -- {}".format(tempMsg[:32], tempMsg[32:]))
  pL = tempMsg[:32]
  pR = tempMsg[32:]
  for i in range(NUM_ROUNDS):
    PNew = xor(pL, roundFunction(pR,subkeys[i]))
    pL = pR
    pR = PNew
  pTemp = pR
  pR = pL
  pL = pTemp
  return pR+pL


def FeWencryption(message):
  messages = getBinWords(getHexwords(message))
  # messages = getBinWords(message)
  print("The message in hex is : {}".format(getHexwords(message)))
  subkeys = keyGen("1111111100000000111111110000000011111111000000001111111100000000")
  encrypted_messages = []
  for msg in messages:
    encrypted_messages.append(messageEncryption(msg, subkeys))
  print(encrypted_messages)
  encrypted_message = hex(int(''.join(encrypted_messages), 2))
  return encrypted_message


def FeWDecryption(encrypt):
  pass

 
##########################    END OF ENCRYPTION    #########################################   


if __name__ == "__main__":
    encrypt = FeWencryption("Hi this worked")
    print("The encrypted message is {}".format(encrypt))
    print(FeWDecryption(encrypt))



