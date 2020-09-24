import sys
from pathlib import Path
from PIL import Image
from steganography.cipher.vigenere import extended_vigenere_encrypter, extended_vigenere_decrypter
from steganography.image_steganography import *
from steganography.util import *

resource_path = Path('./steganography')

if __name__ == "__main__":
    '''
    utils
    '''
    # metadata_binary = image_metadata_to_binary(method='lsb', encrypt=False, sequential=True, threshold=0.3, file_size=2000, file_name='test.png')
    # print(metadata_binary)
    # print(binary_to_float('00111110100110011001100110011010'))
    # print(binary_to_int('0000000010111011'))
    # print(binary_to_string('0111010001100101011100110111010000101110011100000110111001100111'))
    # a = b'message'
    # a_bit = bytes_to_bit(a)
    # print(bit_to_bytes(a_bit))
    # metadata_size, method, encrypt, sequential, threshold, embed_file_size, embed_file_name = binary_to_image_metadata('0000000010111011011001111101001100110011001100110100000000000000000000000000000101001110011011010000110111101110010011101000110100001100001011010010111001000101110011100000110111001100111')
    # print(metadata_size)
    # print(method)
    # print(encrypt)
    # print(sequential)
    # print(threshold)
    # print(embed_file_size)
    # print(embed_file_name)
    '''
    cipher
    '''
    # encrypted = extended_vigenere_encrypter(b'message', 'key')
    # temp = bytes_to_bit(encrypted)
    # temp = bit_to_bytes(temp)
    # decrypted = extended_vigenere_decrypter(temp, 'key')
    # print(bytes_to_bit(decrypted))
    # c = BitArray(decrypted).bin[2:]
    # print(c)
    # file_name = resource_path/'sample_files/small.txt'
    # dest = resource_path/'sample_result/new_small.txt'
    # content = None
    # with open(file_name, 'rb') as f:
    #     content = f.read()
    #     encrypted = extended_vigenere_encrypter(content, 'key')
    # temp_bit = bytes_to_bit(encrypted)
    # temp = bit_to_bytes(temp_bit)
    # decrypted = extended_vigenere_decrypter(temp, 'key')
    # with open(dest, 'wb+') as f:
    #     f.write(decrypted)
    '''
    embed to image
    '''
    # embed_to_image(embedded_file="steganography/sample_files/small.txt", cover_file="steganography/sample_images/shorthair.png", key="steganography", method="lsb", encrypt=False, sequential=True)
    extract_from_image(stego_file="steganography/sample_result/shorthair.png", key="steganography")

    '''
    comparing images
    '''
    # with Image.open(resource_path/'sample_result/shorthair.png') as cover_img:
    #     width, height = cover_img.size
    #     for x in range(0, 20):
    #         for y in range(0, 20):
    #             pix = cover_img.getpixel((x,y))
    #             print(pix)
    pass
