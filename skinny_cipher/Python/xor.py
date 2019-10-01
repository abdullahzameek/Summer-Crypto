import csv

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

with open('output1.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        count = 0
        row = str(row).split('\\t')
        r1 = row[0].replace("['","")
        r2 = row[2].replace("']","")
        xored = xor(r1,r2)
        for c in xored:
            if (c == '1'):
                count+=1
        with open('outputxor.csv', 'a') as csv:
            csv.write(r1 + '\t' + r2 + '\t' + xored + '\t' + str(count) + '\n')
            

