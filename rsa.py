# Basic Algorithm Structure:

# Create random big number generator
# Check for primality by LowPrime and MillerRabinTest
# If prime make n = p * q
# Create m = (p - 1) * (q - 1)

# Compute e, coprime of m and very small odd integer
# Compute d, multiplicative inverse of e modulo m
# P(e,n) public key
# S(d,n) private key
# M is the message converted to ASCII
# P(M) = M^e mod n (becomes C - encryption) and S(C) = C^d mod n (becomes M - decryption)
# Implement signatures
# Make presenatation, proofs and compute complexities
# Check for plagarism 

import random

# pre-generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
		     31, 37, 41, 43, 47, 53, 59, 61, 67,
		     71, 73, 79, 83, 89, 97, 101, 103,
		     107, 109, 113, 127, 131, 137, 139,
		     149, 151, 157, 163, 167, 173, 179,
		     181, 191, 193, 197, 199, 211, 223,
		     227, 229, 233, 239, 241, 251, 257,
		     263, 269, 271, 277, 281, 283, 293,
		     307, 311, 313, 317, 331, 337, 347, 349]

# generates a random nBit number
def nBitRandom(n):
	return random.randrange(2**(n-1)+1, 2**n - 1)

# number not divisible by low primes
def getLowLevelPrime(n):
	while True:
		pc = nBitRandom(n)
		for divisor in first_primes_list:
			if pc % divisor == 0 and divisor**2 <= pc:
				break
		else: 
			return pc
# large level prime test
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
    primeCandidateA = getLowLevelPrime(n)
    primeCandidateB = getLowLevelPrime(n)
    if not isMillerRabinPassed(primeCandidateA) and not isMillerRabinPassed(primeCandidateB):
        continue
    else: 
        break

# assert: n = p * q
primeProduct = primeCandidateA * primeCandidateB

# assert: m = (p - 1) * (q - 1)
primeNewProduct = (primeCandidateA-1) * (primeCandidateB-1)

print(primeCandidateA, primeCandidateB)
print(primeProduct, primeNewProduct)
