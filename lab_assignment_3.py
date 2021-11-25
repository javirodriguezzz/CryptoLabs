# Lab Assignment 3
# Javier Rodriguez Campo
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)


def encrypt(key, plaintext):
    # Generate a random 96-bit IV
    iv = os.urandom(16)

    # Construct an AES-128-CBC Cipher object with the given key and
    # randomly generated IV
    encryptor = Cipher(algorithms.AES(key),
                       modes.CBC(iv),
                       backend=default_backend()).encryptor()

    # Encrypt the plaintext and get the associated ciphertext
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return iv, ciphertext


def decrypt(key, iv, ciphertext):
    # Construct a Cipher object, with the key, iv
    decryptor = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    ).decryptor()

    # Decryption gets us the plaintext
    return decryptor.update(ciphertext) + decryptor.finalize()


def parent(index):
    """
    Calculates the paren of a node.
    :param index: Index of the desired node.
    :return: Index of the parent's node.
    """
    return int(index / 2)


def sibling(index):
    """
    Calculates the sibling of a node.
    :param index: Index of the desired node.
    :return: Index of the sibling of the input node.
    """
    if index % 2 == 0:
        return index + 1
    else:
        return index - 1


def siblings_list(node, toret):
    """
    Method to obtain the minimum cover (recursive siblings) of a node.
    :param node: Desired node.
    :param toret: Auxiliary list to append the nodes recursively.
    :return: A list with the index of the nodes of the cover.
    """
    toret.append(sibling(node))
    if parent(node) == 1:
        toret.append(parent(node))
        return toret
    else:
        return siblings_list(parent(node), toret)


def encrypt_without_compromised_nodes(random_key, root_key, content):
    """
    Encrypt without compromised nodes in the tree for visualize the content.
    :param random_key: General key
    :param root_key: Key of node 1
    :param content: Content to encrypt
    """
    iv_key, encrypted_key = encrypt(root_key, random_key)
    content_with_padding = bytes.ljust(content.encode(), 16, b'\0')
    iv_content, encrypted_content = encrypt(random_key, content_with_padding)
    print('Key encrypted with the root key\n' + str(encrypted_key))
    print('Encrypted content with the key\n' + str(encrypted_content))

    decrypted_key = decrypt(root_key, iv_key, encrypted_key)
    print('Decrypted key with the root key\n' + str(decrypted_key))
    decrypted_content = decrypt(decrypted_key, iv_content, encrypted_content)
    print('The decrypted content is --> ' + str(decrypted_content))


def simplified_aacs(message_to_encode, set_of_devices):
    """
    Simulates the AACS standard.
    :param message_to_encode: Desired content to encrypt.
    :param set_of_devices: Binary tree of devices (nodes).
    """
    key_devices = {}
    # Generate a key for each device
    for d in set_of_devices:
        key_devices[d] = os.urandom(16)
    key_devices[1] = root_key = os.urandom(16)

    iv_devices = {}
    encrypted_key_devices = {}
    output = []
    random_key = os.urandom(16)

    # Encrypting without compromised nodes example
    # If any node is compromised--> Just need encrypt with k1
    print('Example of encrypting without compromised devices:')
    encrypt_without_compromised_nodes(random_key, root_key, message_to_encode)

    # Ask about the compromised and access device
    # compromised_device = 10
    compromised_device = int(input('\nNow, select the device which is compromised --> '))

    # access_device = 11
    access_device = int(input('Select the access device --> '))
    # Minimum cover used to re-encrypt the content and header
    cover = list(reversed(siblings_list(compromised_device, [])))

    # For every node u in a cover of S, compute cu ← E(ku, k)
    # Encrypt the general key with each node key of the cover
    for c in cover:
        iv_devices[c], encrypted_key_devices[c] = encrypt(key_devices[c], random_key)
        output.append(encrypted_key_devices[c])

    # Encrypt the content
    # Add the padding for the block cipher
    message_bytes = bytes.ljust(message_to_encode.encode(), 16, b'\0')
    iv_content, encrypted_content = encrypt(random_key, message_bytes)
    # output.append(encrypted_content)

    # Apply encrypt/decrypt operations to verify with each key in the header
    try:
        for encrypted_header in output:
            decrypted_key = decrypt(key_devices[access_device], iv_devices[access_device], encrypted_header)
            decrypted_content = decrypt(decrypted_key, iv_content, encrypted_content)
            if decrypted_content == message_bytes:
                print('Access allowed with device ' + str(access_device))
                print('Decrypted content: ' + str(decrypted_content))
    except Exception:
        print('Access denied with device ' + str(access_device) + ', the key is compromised!')


simplified_aacs('plaintext', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
