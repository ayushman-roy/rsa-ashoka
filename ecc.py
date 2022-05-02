import hashlib
import random
from ellipticcurve import *
from pyfinitefield import *


def generate_key_pair(order_n, base_G):

    # function should be sound once mult is implemented in a finite field
    private_k = random.SystemRandom().randint(0, order_n-1)
    public_k = private_k * base_G
    return private_k, public_k


def compute_signature(m, base_G, order_n, private_k):

    n_field = FiniteField(order_n, 1)

    # step 1: generate hash of message
    hash_obj = hashlib.sha256()
    hash_obj.update(m.encode())
    hm = int(hash_obj.hexdigest(), 16)

    k = random.SystemRandom().randint(0, order_n-1)
    point_r = k * base_G
    s = n_field(k).inverse() * (n_field(hm) + (n_field(private_k) * point_r.x))

    return hm, point_r, s


def verify_signature(hm, base_G, order_n, public_k):

    n_field = FiniteField(order_n, 1)

    s_inv = n_field(s).inverse()
    u1 = s_inv * n_field(hm)
    u2 = s_inv * n_field(point_r.x)
    kG = int(u1) * base_G + int(u2) * public_k

    return kG.x == point_r.x



def sendDH(privateKey, generator, sendFunction):
    return sendFunction(privateKey * generator)


def receiveDH(privateKey, receiveFunction):
    return privateKey * receiveFunction()


if __name__ == "__main__":

    print("Operating on the bitcoin curve Secp256k1")

    # mutually agreed upon parameters c, G, p, n
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    field = FiniteField(p, 1)
    E = EllipticCurve(a=field(0), b=field(7))
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    G = Point(E, field(Gx), field(Gy))

    # alice writes message, generates her keys, and computes her signature
    message = input("Enter your message: ")
    # generated keys
    private_key, public_key = generate_key_pair(n, G)
    print(f"This is your private key, keep it safe: {private_key}")
    print(f"This is the public key to be published to Bob: {public_key.__list__()}")

    # signature
    hm, point_r, s = compute_signature(message, G, n, private_key)
    if (not point_r.x) or (not s):
        r, s, hm = compute_signature(message, G, n, private_key)
    print(f"This is the message hash to be transmitted to Bob: {hm}")
    print(f"This is the signature for your message:")
    print(f"signature bit 1 (r): {point_r.x}")
    print(f"signature bit 2 (s): {s}")

    # the set exposed to the public is:
    # the message hash hm, the public key, the digital signature, and the base point

    print("____________________________\n")
    # bob verifies signature and proves that alice had her private key and the message using her public key
    print(verify_signature(hm, G, n, public_key))

    '''alice_key = random.SystemRandom().randint(0, n-1)
    bob_key = random.SystemRandom().randint(0, n-1)
    alicePublicKey = sendDH(alice_key, G, lambda x: x)
    bobPublicKey = sendDH(bob_key, G, lambda x: x)
    sharedSecret1 = receiveDH(bob_key, lambda: alicePublicKey)
    sharedSecret2 = receiveDH(alice_key, lambda: bobPublicKey)
    print('Shared secret is %s == %s' % (sharedSecret1.x, sharedSecret2.x))

    alice_private, alice_public = generate_key_pair(n, G)
    bob_private, bob_public = generate_key_pair(n, G)

    alice_message = int(''.join([str(ord(c)) for c in "hello bob"]))
    print((alice_message * G).x)
    k = random.SystemRandom().randint(0, n - 1)
    cipher_text = (k * G, (alice_message * G) + (k * bob_public))
    bob_rec = cipher_text[1] - (bob_private * cipher_text[0])
    print(bob_rec.x)'''
