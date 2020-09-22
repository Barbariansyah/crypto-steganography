''' Vignere Cipher '''

from ..helper.vigenere_helper import generate_vigenere_standard_key

def extended_vigenere_encrypter(plaintext, key):
    ciphertext = []
    key = generate_vigenere_standard_key(plaintext, key)
    for i in range(len(plaintext)):
        encrypted_char = (plaintext[i] + ord(key[i])) % 256
        ciphertext.append(encrypted_char)

    return bytes(ciphertext)

def extended_vigenere_decrypter(ciphertext, key):
    plaintext = []
    key = generate_vigenere_standard_key(ciphertext, key)
    if (type(ciphertext) == str) :
        ciphertext = [ord(i) for i in ciphertext]
    for i in range(len(ciphertext)):
        decrypted_char = (ciphertext[i] - ord(key[i])) % 256
        plaintext.append(decrypted_char)

    return bytes(plaintext)