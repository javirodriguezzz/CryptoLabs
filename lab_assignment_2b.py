# Lab Assignment 2b
# Javier Rodriguez Campo
import random
import threading


def primes_in_range(x, y):
    prime_list = []
    for n in range(x, y):
        is_prime = True

        for num in range(2, n):
            if n % num == 0:
                is_prime = False

        if is_prime:
            prime_list.append(n)

    return prime_list


def parallel_prg(seeds_vector):

    def worker(s):
        random.seed(s)
        sequence.append("{:05b}".format(random.randint(0, 31)))

    # PRG de 20b entonces 5bit/bloque, se necesitan 4 seeds
    sequence = []
    for s in seeds_vector:
        t = threading.Thread(target=worker, args=(s,))
        t.start()

    print(sequence)


def blum_micali_prg(initial_seed):
    next_seed = initial_seed
    prime_list = primes_in_range(1, 2000)
    p = random.choice(prime_list)
    n = 5
    sequence = []

    print('Initial seed: ' + str(next_seed) + '\nRandom prime number: ' + str(p))
    for i in range(n):
        random.seed(next_seed)
        next_seed = random.randrange(1, 500)

        if next_seed <= (p-1)/2:
            sequence.append(0)
        else:
            sequence.append(1)
        s = next_seed

    print('Sequence of n(' + str(n) + ') pseudorandom numbers: ' + str(sequence))


blum_micali_prg(1000)
parallel_prg([10, 20, 30, 40])

