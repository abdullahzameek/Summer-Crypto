'''
For the use of the S-Box, do the following: 

Input : 0111011000000001

                     A     B      C      D
Let the input be : 0111 | 0110 | 0000 | 0001

Do the following: 
R1 = S0(A) = S0[7] = 15 = 1111
R2 = S1(B) = S1[6] = 7 = 0111
R3 = S2(C) = S2[0] =  2 = 0010
R4 = S3(D) = S3[1] = 4 = 0100


Therefore the output is 1111|0111|0010|0100 

Output : 1111011100100100

'''

S0 = [7, 12, 14, 9, 2, 1, 5, 15, 11, 6, 13, 0, 4, 8, 10, 3]
S1 = [4, 10, 1, 6, 8, 15, 7, 12, 3, 0, 14, 13, 5, 9, 11, 2]
S2 = [2, 15, 12, 1, 5, 6, 10, 13, 14, 8, 3, 4, 0, 11, 9, 7]
S3 = [15, 4, 5, 8, 9, 7, 2, 1, 10, 3, 0, 14, 6, 12, 13, 11] 


'''
In this task, you will implement the S-Box (the S stands for substitution) 
mechanism that is found in most ciphers. 

For a given binary string input (use 011101100000001), use the 4 S-Boxes above to perform a substitution.
1) Break the input string into 4 equally sized chunks of four.
2) Perform the substitution as follows :
     Let 0111 be the first chunk. The substitution for this chunk comes from S0
     Convert 0111 to decimal. (You get 7)
     Get the element on the 7th index from the list S0. (The element is 15)
     Convert that element to binary. (15 corresponds to 1111)
     The binary value of the previous step is the new binary value to be substituted. 
     Repeat for the remaining 3 chunks. 


'''



def SBoxSubstitution(inputString):


    return outputString