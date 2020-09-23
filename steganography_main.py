import sys
from steganography.cipher.vigenere import extended_vigenere_encrypter
from steganography.image_steganography.lsb import *
from steganography.util import *

if __name__ == "__main__":
    # metadata_binary = image_metadata_to_binary(method='lsb', encrypt=False, sequential=True, threshold=0.3, file_size=2000, file_name='test.png')
    # print(metadata_binary)
    # print(binary_to_float('00111110100110011001100110011010'))
    # print(binary_to_int('00000000000000000000011111010000'))
    # print(binary_to_string('0111010001100101011100110111010000101110011100000110111001100111'))
    embed_to_image(embedded_file="steganography/sample_images/small-kanye.png", cover_file="steganography/sample_images/shorthair.png", key="steganography", method="lsb", encrypt=True, sequential=True)
    pass
