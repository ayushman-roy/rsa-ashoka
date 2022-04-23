import random
import time

# Fermat's Theorem: if for every i between 1 < i < n-1, a^(n-1) % n = 1, then n is prime

def isPrimeA(n):
    if n <= 1:
        return False
    elif n % 2 == 0 or n % 3 == 0 or n % 5 == 0:
        if n == 2 or n == 3 or n ==5:
            return True
        return False
    checker = True
    i = 2
    while i < n-1 and checker:
        if (i**(n-1)) % n != 1:
            checker = False            
        i += 1
    if checker == True:
        return True
    else: 
        return False

def isPrimeB(n):
    if n <= 1:
        return False
    elif n == 2 or n == 3:
        return True
    checker = True
    i = 2
    while i < n-1 and checker:
        if (i**(n-1)) % n != 1:
            checker = False            
        i += 1
    if checker == True:
        return True
    else: 
        return False
    
def largePrimes():
    while True:
        largeNumA = random.randrange((2**329)+1, (2**330)-1)
        if isPrimeB(largeNumA):
            while True:
                largeNumB = random.randrange((2**329)+1, (2**330)-1)
                if primeCheck(largeNumB):
                    return [largeNumA, largeNumB]

m = 99991
n = 123

end = time.time()
print(largePrimes())
print(end - start)
