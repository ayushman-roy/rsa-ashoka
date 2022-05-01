# Algorithm:

# Create random big number generator
# Check for primality by LowPrime and MillerRabinTest
# If prime make n = p * q
# Create m = (p - 1) * (q - 1)
# Compute e, coprime of m and very small odd integer
# Compute d, multiplicative inverse of e modulo m 					
# P(e,n) public key
# S(d,n) private key
# Create M, the message converted to ASCII 							
# P(M) = M^e mod n = C (encryption) 
# S(C) = C^d mod n = M (decryption)
# Make presentation, proofs and compute complexities for all code 	(LEFT)

# fix decryption
# make plagarism proof

import random
import time

startTime = time.time()

# pre-generated primes for low level prime test
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
		     31, 37, 41, 43, 47, 53, 59, 61, 67,
		     71, 73, 79, 83, 89, 97, 101, 103,
		     107, 109, 113, 127, 131, 137, 139,
		     149, 151, 157, 163, 167, 173, 179,
		     181, 191, 193, 197, 199, 211, 223,
		     227, 229, 233, 239, 241, 251, 257,
		     263, 269, 271, 277, 281, 283, 293,
		     307, 311, 313, 317, 331, 337, 347, 349]

# generates a random n bit number
def randomGenerator(n):
	return random.randrange(2**(n-1)+1, 2**n - 1)

# numbers not divisible by low primes
def lowLevelPrimeCheck(n):
	while True:
		p = randomGenerator(n)
		for divisor in first_primes_list:
			if p % divisor == 0 and divisor**2 <= p:
				break
		else: 
			return p

# higher level prime test by Miller Rabin Test
def isMillerRabinPassed(n):
	maxDivisionsByTwo = 0
	ec = n-1
	while ec % 2 == 0:
		ec >>= 1
		maxDivisionsByTwo += 1
	assert(2**maxDivisionsByTwo * ec == n-1)
	def trialComposite(round_tester):
		if pow(round_tester, ec, n) == 1:
			return False
		for i in range(maxDivisionsByTwo):
			if pow(round_tester, 2**i * ec, n) == n-1:
				return False
		return True
	numberOfRabinTrials = 100
	for i in range(numberOfRabinTrials):
		round_tester = random.randrange(2, n)
		if trialComposite(round_tester):
			return False
	return True

# generates large primes
while True:
    n = 50
    primeCandidateA = lowLevelPrimeCheck(n)
    primeCandidateB = lowLevelPrimeCheck(n)
    if not isMillerRabinPassed(primeCandidateA) and not isMillerRabinPassed(primeCandidateB):
        continue
    else: 
        break

# assert: n = p * q
primeProduct = primeCandidateA * primeCandidateB

# assert: m = (p - 1) * (q - 1)
primeNewProduct = (primeCandidateA-1) * (primeCandidateB-1)

print("Generated Primes: ", primeCandidateA, primeCandidateB)
print("N = p * q and M = (p-1) * (q-1): ", primeProduct, primeNewProduct)

def gcd(p,q):
    while q != 0:
        p, q = q, p%q
    return p

# if gcd = 1, then coprime
def isCoPrime(x, y):
    return gcd(x, y) == 1

# checks if e, m are coprimes
while True:
	e = random.randrange(2, 25)
	if isCoPrime(primeNewProduct, e):
		break

# calculates d, the multiplicative inverse of e modulo m
def modInverse(a, m):
	m0, x, y = m, 1, 0
	if (m == 1):
		return 0
	while (a > 1):
		# q is quotient
		q = a // m
		t = m
		# m is remainder now, same as Euclid
		m = a % m
		a, t = t, y
		# update x and y
		y = x - q * y
		x = t
	# makes x positive
	if (x < 0):
		x = x + m0
	return x

d = modInverse(e, primeNewProduct)

# keys
publicKey = (e, primeProduct)
privateKey = (d, primeProduct)

print("Keys: ", publicKey, privateKey)

# converts message to ASCII as a list
def messageToASCIIConversion(message):
	M = []
	for i in message:
		# M.append((f'{ord(i):03d}'))
		M.append(ord(i))
	return M

# user input: message
message = input("Enter Your Message Here: ")

# conversion to ASCII
convertedMessage = messageToASCIIConversion(message)
print("ASCII Message: ", convertedMessage)

# Iterative Function to calculate
# (x^y)%p in O(log y)
def power(x, y, p) :
	res = 1	 # Initialize result
	# Update x if it is more
	# than or equal to p
	x = x % p
	if (x == 0) :
		return 0
	while (y > 0) :
		# If y is odd, multiply
		# x with result
		if ((y & 1) == 1) :
			res = (res * x) % p
		# y must be even now
		y = y >> 1	 # y = y/2
		x = (x * x) % p
	return res

# encryption: P(M) = M^e mod n = C
def encryption(M):
	encryptedList = M
	index = len(M) - 1
	while(index >= 0):
		message = encryptedList[index]
		ciphertext = power(message, e, primeProduct)
		encryptedList[index] = ciphertext
		if (index >= 1):
			encryptedList[index-1] += ciphertext
		index -= 1
	return encryptedList

def newenc(M):
	cipherlist = []
	for val in M:
		numlist = list(map(int, str(val)))
		encList = numlist
		index = len(numlist) - 1
		while(index >= 0):
			message = numlist[index]
			ciphertext = power(message, e, primeProduct)
			encList[index] = ciphertext
			if (index >= 1):
				numlist[index-1] += ciphertext
			index -= 1
		cipherlist.append(encList)
	return cipherlist

encryptedMessage = encryption(convertedMessage)
print("Encrypted Message:", encryptedMessage)

'''
# password for initiating decryption
password = "1234"

# user prompt for decryption
decryptionInput = input("Do You Want To Decrypt The Message? \nEnter Y for Yes and N for No: ")
if(decryptionInput == "Y" or "y"):
	askPassword = True

# password checker
while askPassword:
		userPassword = input("Enter The Password: ")
		if (userPassword == password):
			askPassword = False
'''

# decryption: S(C) = C^d mod n = M
def decryption(C):
	decryptedList = C
	temp = 0
	index = len(C) - 1
	while(index >= 0):
		ciphertext = decryptedList[index]
		# decryptedList[index] -= temp
		message = power(ciphertext, d, primeProduct)
		# decryptedList[index] += message
		decryptedList[index] = message - temp
		if (index >= 1):
			temp = ciphertext
		index -= 1
	return decryptedList
# (ciphertext**d) % primeProduct

def oldec(c):
	declist = c
	temp = 0
	index = 0
	while (index < len(c)):
		ciphertext = c[index]
		message = power(ciphertext, d, primeProduct)
		index += 1
		message = message - int(oldec(c[index:])[index])
	return declist
		
def newdec(C):
	messageList = []
	for cipher in C:
		declist = [0, 0, 0]
		temp = 0
		index = len(cipher)-1
		while (index >= 0):
			ciphertext = cipher[index]
			message = power(ciphertext, d, primeProduct)
			declist[index] = message - temp
			if (index >= 1):
				temp = ciphertext
			index -= 1
		messageList.insert(0,declist)
	return messageList

decryptedMessage = decryption(encryptedMessage)
# decryptedMessage = newdec(encryptedMessage)
print("Decrypted Message (ASCII): ", decryptedMessage)

# converts ASCII list to message string 
def ASCIIToMessageConversion(message):
	R = ""
	for val in message:
		R += chr(val)
	return R

# returns the decrypted message as string
finalmessage = ASCIIToMessageConversion(decryptedMessage)
print("The Message Receieved Was: ", finalmessage)
print("Time Elapsed: ", time.time() - startTime)
