#create random big num gen
#check for primality by mod 2,3,5 and millerrabintest
#if prime make n=pq
#assert m=(p-1)*(q-1)

#day2 
#make github
#compute e, coprime of m and v small odd int
#compute d, mul inv of e modulo m
#P(e,n) pubkey
#S(d,n) pvt key
#M is the message converted to ASCII
#P(M) = M^e mod n (becomes C - encrypts) and S(C) = C^d mod n (becomes M)

#day3
#after creation of RSA v1.0 make it faster as per instructions and implement signatures

#day4
#make presenatation and full code check, project end

import random

# Fermat's Theorem: if for every i between 1 < i < n-1, a^(n-1) % n = 1, then n is prime
def primeCheck(n):
    if n <= 1 or n % 2 == 0 or n % 3 == 0 or n % 5 == 0:
        return False
    checker = True
    i = 2
    while i < n-1 and checker:
        if (i**n-1) % n != 1:
            checker = False            
        i += 1
    if checker == True:
        return True
    else: 
        return False

def largePrimes():
    while True:
        largeNumA = random.randrange((2**329)+1, (2**330)-1)
        if primeCheck(largeNumA):
            while True:
                largeNumB = random.randrange((2**329)+1, (2**330)-1)
                if primeCheck(largeNumB):
                    return [largeNumA, largeNumB]

primes = largePrimes()        
n = primes[0] * primes[1]
m = (primes[0]-1) * (primes[1]-1)

# def rsaCrypto(message):