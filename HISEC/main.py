import sys
import bitarray

"""
HISEC
Messages encrypted in 64 bit blocks
80 bit key over 15 rounds
"""

####################################### s-box #######################################

sbox = [15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4] 

################################# generic functions #################################

# Converts a string to a bits format
def stringToBits(string_input):
  string_output = bitarray.bitarray()
  string_output.frombytes(string_input.encode("utf-8"))
  return string_output.to01()

def create_messages(message):
    messages = []
    bits_msg = stringToBits(message)
    for i in range(0, len(bits_msg), 64):
        msg = bits_msg[i:i+64]
        msg += ''.join(['0']*(64-len(msg)))
        messages.append(msg)
    return messages

# Shift array to the left by val
def rotate_left(array, val):
    shift = val % 32
    return array[shift:]+array[:shift]

# Generic xor function
def xor(val1, val2):
    if (len(val1) != len(val2)):
        print("Failure to xor due to unequal lengths in input.")
        sys.exit()
    xored = []
    for i in range(len(val1)):
        bit1 = int(val1[i])
        bit2 = int(val2[i])
        xorBit = int(bool(bit1) ^ bool(bit2))
        xored.append(xorBit)
    return ''.join(map(str,xored))

################################## generating subkeys ###############################

def generateSubkeys(key):
    subkeys = []
    print("Generating Subkeys...")
    bitKey = stringToBits(key)
    for i in range(15):
        bitKey = rotate_left(bitKey, 13+(i*2))
        subkeys.append(bitKey[16:])
        print("Subkey #{0:02d} is {1}".format(i+1, subkeys[i]))
    return subkeys

############################# round function components #############################

# Layer 1 is pretty trivial its just an xor tbh...
def layer1(msg, key):
    return xor(msg, key)

# S box layer for the 32 bit values
def layer2(msg):
    leftOut = []
    rightOut = []
    lmsg = msg[:32]
    rmsg = msg[32:]
    leftList = [lmsg[i:i+4] for i in range(0,32,4)]
    rightList = [rmsg[i:i+4] for i in range(0,32,4)]
    for i in range(8):
        a = int(leftList[i],2)
        b = int(rightList[i],2)
        leftOut.append(str(format(sbox[a],"b")).zfill(4))
        rightOut.append(str(format(sbox[b],"b")).zfill(4))
    
    return ''.join(leftOut), ''.join(rightOut)

# diffusion layer for reordering of bits
def layer3(left, right):
    pleft = []
    pright = []
    for i in range(4):
        for j in range(8):
            pleft.append(left[i+j*4])
            pright.append(right[i+j*4])

    return ''.join(pleft), ''.join(pright)

# more xor-ing and left shifting
def layer4(left, right):
    left = xor(rotate_left(left, 20), right)
    right = xor(rotate_left(right, 20), left)
    return left+right

##################################### encryption ####################################

def roundFunction(messages, keys):
    encrypted = []
    for msg in messages:
        for i in range(15):
            up_msg = layer1(msg, keys[i])
            lmsg, rmsg = layer2(up_msg)
            lmsg, rmsg = layer3(lmsg, rmsg)
            up_msg = layer4(lmsg, rmsg)
        encrypted.append(up_msg)
    return hex(int(''.join(encrypted), 2))

##################################### testing #######################################

def test():
    subkeys = generateSubkeys("Testings!!")
    messages = create_messages("this is such a nice message!")
    print(hex(int(''.join(messages),2)))
    encrypted = roundFunction(messages, subkeys)
    print(encrypted)

if __name__ == "__main__":
    test()