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
    # print(binary_to_string('01110110011001010111001001111001001000000111001101101101011000011011011000100010111100101111000000110010000000100100000101100001'))
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
    # print(random_unique_location(19, 20, 2, 30, 30))

    # print(int_to_binary(255))

    # with Image.open(resource_path/'sample_images/shorthair.png') as cover_img:
    #     blocks = cover_to_blocks(cover_img)

    # print(len(blocks))
    # print(len(blocks[0]))
    # print(len(blocks[0][0]))
    # #8 x 8
    # print(len(blocks[0][0][0]))
    # print(len(blocks[0][0][0][0]))
    # print(blocks[0][0])
    # bitplane = block_to_bitplane(blocks[0][0])
    # print(bitplane) 24 x 8 x 8
    # print(len(bitplane))
    # print(len(bitplane[0]))
    # print(len(bitplane[0][0]))

    # bitplane = [
    #     [0,0,0,0,0,0,0,1],
    #     [0,0,0,0,0,0,0,0],
    #     [1,0,1,1,0,0,0,1],
    #     [1,0,0,1,0,0,0,1],
    #     [1,0,0,0,0,0,0,1],
    #     [0,0,0,1,0,0,0,0],
    #     [0,0,1,0,1,0,0,0],
    #     [0,0,0,1,0,0,0,0]
    #     ]
    # print(count_bitplane_complexity(bitplane))
    # cgc = bitplane_pbc_to_cgc(bitplane)
    # pbc = bitplane_cgc_to_pbc(cgc)

    # print(cgc)
    # print(pbc)
    # print(bitplane == pbc)

    # conjugation = conjugate_block_with_wc(bitplane)
    # reconjugated = conjugate_block_with_wc(conjugation)
    # print(bitplane == reconjugated)
    # print(count_bitplane_complexity(conjugation))

    # message = '11010011' * 8
    # message_blocks = message_bin_to_blocks(message)
    # print(message_blocks)
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
    embed to image lsb
    '''
    # embed_to_image(embedded_file="steganography/sample_files/small.txt", cover_file="steganography/sample_images/shorthair.png", key="steganography", method="lsb", encrypt=False, sequential=True)
    # extract_from_image(stego_file="steganography/sample_result/shorthair.png", key="steganography")

    # embed_to_image(embedded_file="steganography/sample_files/small.txt", cover_file="steganography/sample_images/shorthair.png", key="steganography", method="lsb", encrypt=False, sequential=False)
    # extract_from_image(stego_file="steganography/sample_result/shorthair.png", key="steganography")

    # embed_to_image(embedded_file="steganography/sample_files/small.txt", cover_file="steganography/sample_images/cat.bmp", key="steganography", method="lsb", encrypt=True, sequential=True)
    # extract_from_image(stego_file="steganography/sample_result/cat.bmp", key="steganography")

    # embed_to_image(embedded_file="steganography/sample_files/small.txt", cover_file="steganography/sample_images/cat.bmp", key="steganography", method="lsb", encrypt=True, sequential=False)
    # extract_from_image(stego_file="steganography/sample_result/cat.bmp", key="steganography")
    '''
    embed to image bpcs
    '''
    embed_to_image(embedded_file="steganography/sample_files/small.txt", cover_file="steganography/sample_images/shorthair.png", key="steganography", method="bpcs", encrypt=False, sequential=True)
    # embed_to_image(embedded_file="steganography/sample_files/small.txt", cover_file="steganography/sample_images/cat.bmp", key="steganography", method="bpcs", encrypt=True, sequential=True)
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
