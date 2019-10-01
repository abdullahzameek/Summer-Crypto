'''
Implementation of DES
'''

################################################  INITIAL CONSTANTS BEGIN HERE ###########################################################
import sys
import bitarray

# First Key Permutation done on the 64 bit key to retreieve a 56 bit version
PC1 = [57,  49,  41,  33,  25,  17,   9,
        1,  58,  50,  42,  34,  26,  18,
       10,   2,  59,  51,  43,  35,  27,
       19,  11,   3,  60,  52,  44,  36,
       63,  55,  47,  39,  31,  23,  15,
        7,  62,  54,  46,  38,  30,  22,
       14,   6,  61,  53,  45,  37,  29,
       21,  13,   5,  28,  20,  12,   4]

# Left shift each subsequent subkey (from C0-D0) to get the required 16 subkeys
LSHIFT_MAP = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# Second Key Permutation done on the concatenated 56 bit key to obtain a 48 bit subkey
PC2 = [14,  17,  11,  24,   1,   5,
       3,   28,  15,   6,  21,  10,
       23,  19,  12,   4,  26,   8,
       16,   7,  27,  20,  13,   2,
       41,  52,  31,  37,  47,  55,
       30,  40,  51,  45,  33,  48,
       44,  49,  39,  56,  34,  53,
       46,  42,  50,  36,  29,  32]

# Initial Permutation of the message
IP = [58,  50,  42,  34,  26,  18,  10,   2,
      60,  52,  44,  36,  28,  20,  12,   4,
      62,  54,  46,  38,  30,  22,  14,   6,
      64,  56,  48,  40,  32,  24,  16,   8,
      57,  49,  41,  33,  25,  17,   9,   1,
      59,  51,  43,  35,  27,  19,  11,   3,
      61,  53,  45,  37,  29,  21,  13,   5,
      63,  55,  47,  39,  31,  23,  15,   7]

# Extending 32 bit R_n-1 to a 48 bit version to correspond to subkey size
E = [32,   1,   2,   3,   4,   5,
      4,   5,   6,   7,   8,   9,
      8,   9,  10,  11,  12,  13,
     12,  13,  14,  15,  16,  17,
     16,  17,  18,  19,  20,  21,
     20,  21,  22,  23,  24,  25,
     24,  25,  26,  27,  28,  29,
     28,  29,  30,  31,  32,   1]

# Substituting back to get a 32 bit value
# Done by splitting the 48 bit into 6 bit segments, 
# The first and last bit are considered the row number
# The middle 4 bits are the column number
SBOXES = {0:
            [[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
             [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
             [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
             [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]],
          1:
            [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
             [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
             [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
             [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]],
          2:
            [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
             [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
             [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
             [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],
          3:
            [[ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
             [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
             [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
             [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],
          4:
            [[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
             [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
             [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
             [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]],
          5:
            [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
             [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
             [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
             [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],
          6:
            [[ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
             [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
             [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
             [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],
          7:
            [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
             [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
             [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
             [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]}

# Permutes the sbox value for the final 32 bit value that is then added on top of the L_n-1 value
P = [16,   7,  20,  21,
     29,  12,  28,  17,
      1,  15,  23,  26,
      5,  18,  31,  10,
      2,   8,  24,  14,
     32,  27,   3,   9,
     19,  13,  30,   6,
     22,  11,   4,  25]

# A final permutation that is placed on the reverse concatenated R_16 L_16 bit string
IP_INVERSE = [40,   8,  48,  16,  56,  24,  64,  32,
              39,   7,  47,  15,  55,  23,  63,  31,
              38,   6,  46,  14,  54,  22,  62,  30,
              37,   5,  45,  13,  53,  21,  61,  29,
              36,   4,  44,  12,  52,  20,  60,  28,
              35,   3,  43,  11,  51,  19,  59,  27,
              34,   2,  42,  10,  50,  18,  58,  26,
              33,   1,  41,   9,  49,  17,  57,  25]
              
#######################################################  END OF CONSTANTS  ########################################################################

#######################################################  GENERIC FUNCTIONS ########################################################################

#convert string to a hexadecimal representation
def stringToHex(stringInput):
  return ''.join(hex(ord(x))[2:] for x in stringInput) 

#for a given string, convert it to hex and partition it in 64bit words and add padding if needed (Padding is just zeroes)
def getHexwords(msg):
    """break the ASCII message into a 64bit (16 hex bytes) words"""
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

#take a list of hex Words and convert each of them to binary. 
def getBinWords(hexWords):
  binWords = []
  for message in hexWords:
    binWord = hexToBinary(message)
    binWords.append(binWord)
  return binWords


# XORs two bit values val1 and val2
def xor(val1, val2):
  xoredBits = [] 
  for i in range(len(val1)):
    bit1 = int(val1[i])
    bit2 = int(val2[i])
    xorBit = int(bool(bit1) ^ bool(bit2))
    xoredBits.append(xorBit)
  return ''.join(map(str,xoredBits))

########################################################## KEY FUNCTIONS ##########################################################################

def generate_subkeys(key):
  key_bits = hexToBinary(key)
  if len(key_bits) != 64:
    print("Incorrect key provided.")
    sys.exit()
  key_up = []
  for i in range (56):
    key_up.append(key_bits[PC1[i]-1])
  key_up = ''.join(key_up)
  print("The initial key is {}".format(key_bits))
  print("They permuted key is {}".format(key_up))
  
  subkeys = []

  left = key_up[:28]
  right = key_up[28:]
  print(left)
  print(right)

  for i in range(16):
    left = leftshift(left, LSHIFT_MAP[i])
    right = leftshift(right, LSHIFT_MAP[i])
    subkey = left + right
    subkey_final = []
    for j in range(48):
      subkey_final.append(subkey[PC2[j]-1])
    subkeys.append("".join(subkey_final))
    
  for i in range (16):
    print("Subkey #{} is {}".format(i+1,subkeys[i]))

  print("the length is : {}".format(len(subkeys[0])))
  print("Keys have been generated.")  
  return subkeys

 
############################################################### END OF KEY FUNCTIONS #########################################################


############################################################### ENCODING STARTS HERE #########################################################



#take a list of binary words and permute them according to IP. Returns a list of binaries as strings. 
def permute(binMessageList):
  permutedList = []
  temp = []
  for message in binMessageList:
      for elem in IP:
        temp.append(message[int(elem)-1])
      strTemp = ''.join(map(str,temp))
      permutedList.append(strTemp)
  return permutedList


# Run 8 rounds of S-box with the given 48 bit value
def sbox_substitution(mixed_R):
  reducedR = []
  splitList = []
  bitList = list(mixed_R)
  #create 8 lists of 6 elems 
  splitList = [bitList[i:i + 6] for i in range(0, len(bitList), 6)]
  for i in range(8):
    row = int(splitList[i][0] + splitList[i][-1],2)
    col = int(splitList[i][1] + splitList[i][2] + splitList[i][3] + splitList[i][4],2)
    newVal = SBOXES[int(i)][row][col]
    bits = str(format(newVal,"b")).zfill(4) 
    reducedR.append(bits)
  return ''.join(reducedR)
  
#Input an individual 64 bit message into to get encrypted
def message_encryption(message, subkeys):
  temp_msg = message
  print("the full message is : {}".format(temp_msg))
  print("The message is {} -- {}".format(temp_msg[:32], temp_msg[32:]))
  L_n = temp_msg[:32]
  R_n = temp_msg[32:]
  L_n1 = temp_msg[:32]
  R_n1 = temp_msg[32:]
  print("L_0 is : {}".format(L_n))
  print("R_0 is : {}".format(R_n))
  for i in range(16):
    L_n = R_n1
    print("L_{} is : {}".format(i+1, L_n))
    expanded_R = []
    for j in range(48):
      expanded_R.append(L_n[E[j]-1])
    mixed_R = xor(subkeys[15], expanded_R)
    reduced_R = sbox_substitution(mixed_R)
    permuted_R = []
    for k in range (32):
      permuted_R.append(reduced_R[P[k]-1])
    R_n = xor(L_n1, permuted_R)
    print("R_{} is : {}".format(i+1, R_n))
    L_n1 = L_n
    R_n1 = R_n
    # temp_msg = L_n + R_n
    
  encrypted_msg = []
  norm = temp_msg[32:] + temp_msg[:32]
  for i in range(64):
    encrypted_msg.append(norm[IP_INVERSE[i]-1])
  
  return ''.join(encrypted_msg)
      

def DESencryption(message):
  messages = getBinWords(getHexwords(message))
  # messages = getBinWords(message)

  print("The message in hex is : {}".format(getHexwords(message)))
  subkeys = generate_subkeys("54657374696e6731")

  encrypted_messages = []
  permute(messages)
  for msg in messages:
    encrypted_messages.append(message_encryption(msg, subkeys))
  encrypted_message = hex(int(''.join(encrypted_messages), 2))
  return encrypted_message


############################################################ END OF ENCODING  #############################################################
  
def test():
  # subkeys = generate_subkeys("133457799BBCDFF1")
  # print(DESencryption("is is a nice time to be alive"))
  # print("\n\n\n")
  print(DESencryption("Today is a good day."))

if __name__ == "__main__":
    test()