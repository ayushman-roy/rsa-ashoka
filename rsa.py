# Algorithm:

# Create random big number generator
# Check for primality by LowPrime and MillerRabinTest
# If prime make n = p * q
# Create m = (p - 1) * (q - 1)
# Compute e, coprime of m and very small odd integer
# Compute d, multiplicative inverse of e modulo m 					(LEFT)
# P(e,n) public key
# S(d,n) private key
# Create M, the message converted to ASCII 							
# P(M) = M^e mod n = C (encryption) 
# S(C) = C^d mod n = M (decryption)
# Implement signatures 												(LEFT)
# Make presentation, proofs and compute complexities for all code 	(LEFT)

import random

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
def isMillerRabinPassed(mrc):
	maxDivisionsByTwo = 0
	ec = mrc-1
	while ec % 2 == 0:
		ec >>= 1
		maxDivisionsByTwo += 1
	assert(2**maxDivisionsByTwo * ec == mrc-1)
	def trialComposite(round_tester):
		if pow(round_tester, ec, mrc) == 1:
			return False
		for i in range(maxDivisionsByTwo):
			if pow(round_tester, 2**i * ec, mrc) == mrc-1:
				return False
		return True
	numberOfRabinTrials = 20
	for i in range(numberOfRabinTrials):
		round_tester = random.randrange(2, mrc)
		if trialComposite(round_tester):
			return False
	return True

# generates large primes
while True:
    n = 100
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

'''
def multiplicative_inverse(e, primeNewProduct):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_p = primeNewProduct
    while e > 0:
        temp1 = temp_p//e
        temp2 = temp_p - temp1 * e
        temp_p = e
        e = temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    if temp_p == 1:
        return d

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m
'''

def modInverse(a, m):
	m0 = m
	y = 0
	x = 1
	if (m == 1):
		return 0
	while (a > 1):
		# q is quotient
		q = a // m
		t = m
		# m is remainder now, process
		# same as Euclid's algo
		m = a % m
		a = t
		t = y
		# Update x and y
		y = x - q * y
		x = t
	# Make x positive
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
		M.append(ord(i))
	return M

# user input: message
message = input("Enter Your Message Here:")

# conversion to ASCII
convertedMessage = messageToASCIIConversion(message)
print("Message in ASCII:", convertedMessage)

# encryption: P(M) = M^e mod n = C
def encryption(M):
	encryptedList = M
	index = len(M) - 1
	while(index >= 0):
		message = M[index]
		ciphertext = (message**e) % primeProduct
		encryptedList[index] = ciphertext
		if (index >= 1):
			encryptedList[index-1] += ciphertext
		index -= 1
	return encryptedList

encryptedMessage = encryption(convertedMessage)
print("Encrypted Message:", encryptedMessage)


# decryption: S(C) = C^d mod n = M
def decryption(C):
	decryptedList = C
	temp = 0
	index = len(C) - 1
	while(index >= 0):
		ciphertext = C[index]
		message = (ciphertext**d) % primeProduct
		decryptedList[index] = message - temp
		if (index >= 1):
			temp = message
		index -= 1
	return decryptedList

decryptedMessage = decryption(encryptedMessage)
print("Decrypted Message: ", decryptedMessage)

#converts ASCII list to message string 
def ASCIIToMessageConversion(message):
	R = ""
	for val in message:
		R += chr(message)
	return R

# returns the decrypted message as string
ASCIIToMessageConversion(decryptedMessage)








