import sys
import bitarray

"""
LEA : Lightweight Block Encryption Algorithm
128 bit plaintext encoded in 32 bit blocks
128/192/256 bit key size with 24/28/32 rounds
"""
constants = ["c3efe9db", "44626b02", "79e27c8a", "78df30ec", 
             "715ea49e", "c785da0a", "e04ef22a", "e5c40957"]

################################# generic functions #################################

# Converts a string to a bits format
def stringToBits(string_input):
  string_output = bitarray.bitarray()
  string_output.frombytes(string_input.encode("utf-8"))
  return string_output.to01()

# Rearrange a single message by the LEA standard 
def rearrange(message):
    split = []
    rearranged = []
    for i in range(0, 128, 32):
        split.append(message[i:i+32])
        rearranged.append(split[-1][24:]+split[-1][16:24]+split[-1][8:16]+split[-1][:8])  

    return ''.join(rearranged)

# Shift array to the left by val
def rotate_left(array, val):
    shift = val % 32
    return array[shift:]+array[:shift]

# Shift array to the right by val
def rotate_right(array, val):
    shift = val % 32
    return array[-shift:]+array[:-shift]

# Function to convert the hexadecimal constants to binary
def hexToBinary(hexstr):
  return str(bin(int(hexstr, 16)))[2:].rjust(32, '0')


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

# Addition mod 2^32 of two 32 bit strings
def addition(val1, val2):
    int1 = int(val1, 2)
    int2 = int(val2, 2)
    fin = ((int1+int2) % (2**32))
    return "{0:032b}".format(fin)

############################ pre encryption manipulation ############################

def create_messages(message):
    messages = []
    bits_msg = stringToBits(message)
    for i in range(0, len(bits_msg), 128):
        msg = bits_msg[i:i+128]
        msg += ''.join(['0']*(128-len(msg)))
        messages.append(msg)
    return messages

def rearr_messages(messages):
    rearr_msg = []
    for i in range(len(messages)):
        rearr_msg.append(rearrange(messages[i]))

    return rearr_msg

def generate_subkeys(key):
    subkeys = []
    for i in range(24):
        subkey = []
        x1 = rotate_left(addition(key[:32],rotate_left(hexToBinary(constants[i%4]),i)), 1)
        x2 = rotate_left(addition(key[32:64],rotate_left(hexToBinary(constants[i%4]),i+1)), 3)
        x3 = rotate_left(addition(key[64:96],rotate_left(hexToBinary(constants[i%4]),i+2)), 6)
        x4 = rotate_left(addition(key[96:],rotate_left(hexToBinary(constants[i%4]),i+3)), 11)
        # print("x1 is {} x2 is {} x3 is {} x4 is {}".format(x1,x2,x3,x4))
        subkeys.append(x1+x2+x3+x2+x4+x2)
        # print(rotate_left(constants[i%4],i))
        # print(addition(key[:32],rotate_left(constants[i%4],i)), 1)
    return subkeys

def encryption(messages, subkeys):
    encrypted = []
    for msg in messages:
        print("Encrypting message : {}".format(msg))
        ### temp vars
        t0 = msg[:32]
        t1 = msg[32:64]
        t2 = msg[64:96]
        t3 = msg[96:]
        for i in range(24):
            x0 = rotate_left(addition(xor(t0,subkeys[i][:32]),xor(t1,subkeys[i][32:64])),9)
            x1 = rotate_right(addition(xor(t1,subkeys[i][64:96]),xor(t2,subkeys[i][96:128])),5)
            x2 = rotate_right(addition(xor(t2,subkeys[i][128:160]),xor(t3,subkeys[i][160:])),3)
            x3 = t0
            print("Round {0:02d} : {1}".format(i+1, x0+x1+x2+x3))
            t0 = x0
            t1 = x1
            t2 = x2
            t3 = x3
        encrypted.append(x0+x1+x2+x3)
        print("The encrypted message is : {}".format(encrypted[-1]))
    
    return hex(int(''.join(encrypted), 2))


##################################### testing #######################################

def test():
    print(constants)
    messages = create_messages("This is a test message.")
    print("The initial message is : {}".format(hex(int(''.join(messages), 2))))
    rearranged_messages = rearr_messages(messages)
    key = rearrange(stringToBits("Thisu key great!"))
    subkeys = generate_subkeys(key)
    encrypt = encryption(rearranged_messages, subkeys)
    print("The complete encrypted message is : {}".format(encrypt))


if __name__ == "__main__":
    test()