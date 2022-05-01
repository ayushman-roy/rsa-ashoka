from Crypto.Util import number
from random import randrange

# generates prime numbers of 1024 bits
primeCandidateA = number.getPrime(1024)
primeCandidateB = number.getPrime(1024)

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
	e = randrange(2, 25)
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
