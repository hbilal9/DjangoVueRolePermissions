# Alpha-numeric characters (0-9, a-z, A-Z)
"""Alpha-numeric characters (0-9, a-z, A-Z)"""
def generate_random_number(length=10):
    import random
    # import string
    random_string = '123456789'
    # for string add string.ascii_letters + string.digits
    return ''.join(random.choice(random_string) for _ in range(length))

# Alpha-numeric characters (0-9, a-z, A-Z)
""" Alpha-numeric characters (0-9, a-z, A-Z) """
def generate_random_string(length=10):
    import random
    # import string
    random_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    # for string add string.ascii_letters + string.digits
    return ''.join(random.choice(random_string) for _ in range(length))



import pickle
# Encryption key
encryption_key = 'HBi7@7Kh@NY0s4Fz4@1'

def encrypt_dict(data):
    # Serialize the dictionary using pickle
    serialized_data = pickle.dumps(data)

    # Perform XOR encryption on each byte of the serialized data
    encrypted_data = bytearray()
    key_length = len(encryption_key)
    for i, byte in enumerate(serialized_data):
        encrypted_byte = byte ^ ord(encryption_key[i % key_length])
        encrypted_data.append(encrypted_byte)

    return encrypted_data.hex()

def decrypt_dict(encrypted_data):
    # Decode the encrypted data from hex encoding
    decoded_data = bytes.fromhex(encrypted_data)

    # Perform XOR decryption on each byte of the data
    decrypted_data = bytearray()
    key_length = len(encryption_key)
    for i, byte in enumerate(decoded_data):
        decrypted_byte = byte ^ ord(encryption_key[i % key_length])
        decrypted_data.append(decrypted_byte)

    try:
        return pickle.loads(decrypted_data)
    except pickle.UnpicklingError:
        # Handle invalid hash exception
        return None