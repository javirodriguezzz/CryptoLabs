# Lab Assignment 4
# Javier Rodriguez Campo

# INITIALIZATION
# Client and Server --> key pair created with the Diffie-Hellman scheme
# Client and Server --> same RootKey (128 bits)


# DOUBLE RATCHET
# Diffie-Hellman ratchet --> use DH for generate (PublicKey, PrivateKey)
#                            use HKDF to ratchet the DH keys (5.2 specification)
#                            policy for new DH keys = after n messages, per session, etc.
# Symmetric key ratchet --> not encrypt the message headers
#                           use HMAC to ratchet the symmetric keys
#                           use AES-GCM (128 bits) to encrypt and decrypt messages
