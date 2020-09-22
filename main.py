from steganography.cipher.vigenere import extended_vigenere_encrypter
from steganography.image_steganography.lsb import *
from steganography.util import *

if __name__ == "__main__":
    '''
    testing embed
    '''
    embed_to_image(embedded_file="steganography/sample_images/small-kanye.png", cover_file="steganography/sample_images/shorthair.png", key="steganography", method="lsb", encrypt=True, sequential=True)


    '''
    testing utils
    '''
    # print(get_file_size("steganography/sample_images/small-shorthair.png"))

    # res = extended_vigenere_encrypter(b'plain teks', 'bari')
    # print(res)
    # print(format(res[0], '08b'))
