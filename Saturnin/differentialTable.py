SIGMA_1 = [0,6,14,1,15,4,7,13,9,8,12,5,2,10,3,11]
SIGMA_2 = [0,9,13,2,15,1,11,7,6,4,5,3,8,12,10,14]

INPUTS = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

Js = [] 
# i is fixed
# j is determined by i XORed with each value from 0 to 15

SIGMA_1_OUTPUTS = []
SIGMA_2_OUTPUTS = []
SIGMA_1_FINAL = []
SIGMA_2_FINAL = []

for i in INPUTS:
    J = []
    for k in range(16):
         J.append(i^k)
    Js.append(J)


for permutedList in Js:
    s1 = []
    s2 = []
    for k in range(len(permutedList)):
        s1.append(SIGMA_1[INPUTS[k]] ^ SIGMA_1[permutedList[k]])
        s2.append(SIGMA_2[INPUTS[k]] ^ SIGMA_2[permutedList[k]])
    SIGMA_1_OUTPUTS.append(s1)
    SIGMA_2_OUTPUTS.append(s2)


for elem in SIGMA_1_OUTPUTS:
    temp = []
    for i in range(len(elem)):
        temp.append(elem.count(i))
    SIGMA_1_FINAL.append(temp)


for elem in SIGMA_2_OUTPUTS:
    temp = []
    for i in range(len(elem)):
        temp.append(elem.count(i))
    SIGMA_2_FINAL.append(temp)


for elem in SIGMA_1_FINAL:
    print(elem)
print("\n")

for elem in SIGMA_2_FINAL:
    print(elem) 