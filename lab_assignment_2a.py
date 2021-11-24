# Lab Assignment 2a
# Javier Rodriguez Campo
import random
import cryptography  # unused because his method don't need a seed and for us is necessary


def random_bit():
    """
    Method for return a random bit (one or zero), like a coin flip.
    :return: 1 or 0
    """
    coin_flip = random.randrange(10)
    if coin_flip >= 5:
        return 1
    else:
        return 0


def bit_commitment_protocol():
    """
    Method for imitate a bit commitment protocol between Bob and Alice.
        1) Bob generates b0
        2) Alice generates b1
        3) Alice sends a random integer (r)
        4) Bob choose a seed and executes the commit function
        5) The program gives and option for lie and see the different scenes
        6) Bob sends his bit and seed to Alice for verify
        7) Alice can verify executing the commit function with the Bob's seed and bit, and
           the random integer (r)
    """
    bob_coin_flip = random_bit()
    print('[Bob] Generating a random bit...\nThe bit is ' + str(bob_coin_flip))
    alice_coin_flip = random_bit()
    print('[Alice] Generating a random bit...\nSending ' + str(alice_coin_flip) + ' to Bob')

    r = random.randint(000000000000, 999999999999)
    print('[Alice] Sending random r (' + str(r) + ') to Bob')

    # Bob outputs c as the commitment string and uses s as the opening string
    bob_seed = 15
    bob_commit = commit(seed=bob_seed, r=r, coin_flip=bob_coin_flip)
    print('[Bob] Commitment string (c) is ' + str(bob_commit))

    # For verify, Bob sends b(coin_flip) and s(bob_seed) to Alice
    if input('¿ Lie ? [Y/N] ') is 'Y':
        if bob_coin_flip == 1:
            bob_coin_flip = 0
        else:
            bob_coin_flip = 1
    print('[Bob] Sending b(' + str(bob_coin_flip) + ') and s(' + str(bob_seed) + ') to Alice for verify')
    # Alice accepts the opening if c = commit(bob_seed, r, coin_flip)
    print('[Alice] Verifying commitment...')
    alice_commit = commit(bob_seed, r, bob_coin_flip)
    if bob_commit == alice_commit:
        print('[Alice] Commitment accepted')
    else:
        print('[Alice] Commitment denied. That is a lie!')


def commit(seed, r, coin_flip):
    """
    Recreates the commit function for the bit commitment protocol.
    Generates a random commitment string 'G(s)' if the bit equals zero, and if bit is one
    the string is the XOR operation between the random commitment string 'G(s)' and a random (r).
    :param seed: random seed
    :param r: random number
    :param coin_flip: bit (zero or one)
    :return: the commitment string (c)
    """
    random.seed(seed)
    rand_g = random.randrange(10000)
    if coin_flip == 0:
        return rand_g
    else:
        return rand_g ^ r


bit_commitment_protocol()
