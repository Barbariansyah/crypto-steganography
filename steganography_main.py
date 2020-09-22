from steganography.cipher.vigenere import extended_vigenere_encrypter

if __name__ == "__main__":
    res = extended_vigenere_encrypter('plain teks', 'bari')
    print(format(res[0], '08b'))
