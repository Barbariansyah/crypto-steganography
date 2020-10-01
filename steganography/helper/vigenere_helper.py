''' Vigenere cipher helper '''


def generate_vigenere_standard_key(text, key):
    key = list(key)
    if len(key) == len(text):
        return key
    elif len(key) > len(text):
        key = key[:len(text)]
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])

    return "".join(key)
