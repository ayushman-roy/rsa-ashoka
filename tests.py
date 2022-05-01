# different versions of prime checker, that although did check for primes but did not do so with good accuracy
# thus, the crypto.util module was used for calculation of primes in final program

import random

# generates a random n bit number for prime check
def randomGenerator(n):
	return random.randrange(2**(n-1)+1, 2**n - 1)

# list of first primes
lowPrimeList = [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 
                151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 
                317, 331, 337, 347, 349 ]

# numbers not divisible by lower primes
def lowLevelPrimeCheck(n, list):
	while True:
		p = randomGenerator(n)
		for divisor in list:
			if p % divisor == 0 and divisor**2 <= p:
				break
		else: 
			return p
		
# Reference: Geek for Geeks
# Miller Rabin test:
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

# Fermat's test:
def checker(a, n, p):
    res = 1
    a = a % p 
    while n > 0:
        if n % 2:
            res = (res * a) % p
            n = n - 1
        else:
            a = (a ** 2) % p
            n = n // 2
    return res % p
def isPrime(n):
    if n == 1 or n == 4:
        return False
    elif n == 2 or n == 3:
        return True
    else:
        for i in range(10000):
            a = random.randint(2, n - 2)
            if checker(a, n - 1, n) != 1:
                return False
    return True

# generates large probable primes
while True:
    n = 330
    primeCandidateA = lowLevelPrimeCheck(n, lowPrimeList)
    primeCandidateB = lowLevelPrimeCheck(n, lowPrimeList)
    if not isMillerRabinPassed(primeCandidateA) and not isMillerRabinPassed(primeCandidateB):
        continue
    else: 
        break
