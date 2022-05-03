import random

# pre-generated primes for low level prime test
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
		     107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
		     227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347]

# generates a random n bit number
def randomGenerator(n):
	return random.randrange(2**(n-1)+1, 2**n - 1)

# numbers not divisible by low primes
def lowLevelPrimeCheck(n, list):
	while True:
		p = randomGenerator(n)
		for divisor in list:
			if p % divisor == 0 and divisor**2 <= p: break
		else: return p

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
	numberOfRabinTrials = 230
	for i in range(numberOfRabinTrials):
		round_tester = random.randrange(2, n)
		if trialComposite(round_tester):
			return False
	return True

# generates large primes
while True:
	n = 330
	# low level prime testing
	primeCandidateA = lowLevelPrimeCheck(n, first_primes_list)
	primeCandidateB = lowLevelPrimeCheck(n, first_primes_list)
	# miller rabin test
	if isMillerRabinPassed(primeCandidateA) and isMillerRabinPassed(primeCandidateB):
		# each prime (except 2 and 3) is next to a multiple of 6 (https://bit.ly/3vYlVgc)
		if (primeCandidateA-1)%6 == 0 or  (primeCandidateA-1)%6 == 0:
			break
		if (primeCandidateB+1)%6 == 0 or  (primeCandidateB+1)%6 == 0:
			break
	else: continue

# assert: n = p * q
primeProduct = primeCandidateA * primeCandidateB

# assert: m = (p - 1) * (q - 1)
primeNewProduct = (primeCandidateA-1) * (primeCandidateB-1)

# calculates gcd
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
		
# Reference: Geek for Geeks
# calculates the multiplicative inverse
def modInverse(a, m):
	m0, x, y = m, 1, 0
	if (m == 1):
		return 0
	while (a > 1):
		q = a // m
		t = m
		m = a % m
		a, t = t, y
		y = x - q * y
		x = t
	if (x < 0):
		x = x + m0
	return x

# d is the multiplicative inverse of e modulo m
d = modInverse(e, primeNewProduct)

# release for encryption
publicKey = (e, primeProduct)
# keep secret for decryption
privateKey = (d, primeProduct)

# converts message to ASCII as a list
def messageToASCIIConversion(message):
	M = []
	for i in message:
		M.append(ord(i))
	return M

# user input: message
message = input("Enter Your Message Here: ")
convertedMessage = messageToASCIIConversion(message)

# Reference: Geek for Geeks
# calculates (x^y)%p
def power(x, y, p) :
	res = 1
	x = x % p
	if (x == 0) :
		return 0
	while (y > 0) :
		if ((y & 1) == 1) :
			res = (res * x) % p
		y = y >> 1	
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

# release encrypted message
encryptedMessage = encryption(convertedMessage)
print("Encrypted Message:", encryptedMessage)

# password for initiating decryption
password = "1234"
while True:
		userPassword = input("Enter The Password For Decryption: ")
		if (userPassword == password):
			break

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

# decrypts the message
decryptedMessage = decryption(encryptedMessage)

# converts ASCII list to message string 
def ASCIIToMessageConversion(message):
	R = ""
	for val in message:
		R += chr(val)
	return R

# returns the decrypted message as string
finalmessage = ASCIIToMessageConversion(decryptedMessage)
print("The Message Receieved Was: ", finalmessage)
