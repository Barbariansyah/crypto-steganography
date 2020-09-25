from pathlib import Path
import os
import struct
from bitarray import bitarray
import random
import math
import numpy as np

root_path = Path('./')

''' Common Utility '''
def seed_generator(key):
    seed = 0
    for c in key:
        seed += ord(c)
    return seed

def random_unique_location(metadata_length, content_length, seed, width, height):
    random.seed(seed)
    location = random.sample(range(metadata_length, width*height*3), content_length)
    return location    

def bytes_to_bit(bytes_input):
    temp = bitarray()
    temp.frombytes(bytes_input)
    return temp.to01()

def bit_to_bytes(bit_input):
    temp = bitarray(bit_input)
    return temp.tobytes()

def calculate_image_capacity(width, height):
    bit_capacity = width * height * 3
    byte_capacity = bit_capacity // 8
    return bit_capacity, byte_capacity

def handle_ascii_file(file):
    # filename = secure_filename(file.filename)
    file_content = file.read()
    # return filename, file_content
    return file_content

def get_file_size(file_name):
    return os.stat(root_path/file_name).st_size

def int_to_binary(integer):
    return format(integer, '08b')

def binary_to_int(binary):
    return int(binary, 2)

def float_to_binary(float_input):
    return bin(struct.unpack('!I', struct.pack('!f', float_input))[0])[2:].zfill(32)

def binary_to_float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

def string_to_binary(string_input):
    return ''.join(format(ord(c), '08b') for c in string_input)

def binary_to_string(binary):
    result = ''
    for i in range(0, len(binary), 8):
        temp = binary[i:i+8]
        result += chr(int(temp, 2))
    return result        

def get_file_name_from_path(path):
    return path.split('/')[-1]

def image_metadata_to_binary(method, encrypt, sequential, threshold, file_size, file_name):
    metadata_binary = ''
    metadata_binary += '0' if method == 'lsb' else '1'
    metadata_binary += '0' if encrypt == False else '1'
    metadata_binary += '0' if sequential == False else '1'
    metadata_binary += float_to_binary(threshold)
    
    metadata_binary += format(file_size, '032b')
    file_name_binary = string_to_binary(file_name)
    metadata_binary += file_name_binary
    
    metadata_length = len(metadata_binary) + 16
    metadata_binary = format(metadata_length, '016b') + metadata_binary 
    
    return metadata_binary
    
def binary_to_image_metadata(metadata_bin):
    metadata_size = binary_to_int(metadata_bin[0:16])
    method = 'lsb' if metadata_bin[16] == '0' else 'bpcs'        
    encrypt = False if metadata_bin[17] == '0' else True
    sequential = False if metadata_bin[18] == '0' else True
    threshold = binary_to_float(metadata_bin[19:51])
    embed_file_size = binary_to_int(metadata_bin[51:83])
    embed_file_name = binary_to_string(metadata_bin[83:])
    return metadata_size, method, encrypt, sequential, threshold, embed_file_size, embed_file_name

def cover_to_blocks(cover_img):
    width, height = cover_img.size
    blocks = [[[] for _ in range(math.ceil(width/8))] for _ in range(math.ceil(height/8))]
    pixels = list(cover_img.getdata())
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    #fill up pseudo pixels
    if len(pixels[0]) % 8 != 0:
        rem = 8 - len(pixels[0]) % 8
        for i in range(height):
            pixels[i] += [(255, 255, 255, 255) * rem]
    if len(pixels) % 8 != 0:
        rem = 8 - len(pixels) % 8
        for i in range(rem):
            pixels.append([(255, 255, 255, 255) * width])

    for x in range(0, width, 8):
        for y in range(0, height, 8):
            temp = []
            for j in range(y, y+8):
                temp.append(pixels[j][x:x+8])
            blocks[y//8][x//8] = temp

    return blocks

def block_to_bitplane(block):
    bitplane = [[[0 for _ in range(8)] for _ in range(8)] for _ in range(24)]
    for x in range(8):
        for y in range(8):
            r, g, b, a = block[y][x]
            pixel_binary = int_to_binary(r) + int_to_binary(g) + int_to_binary(b)
            for idx, c in enumerate(pixel_binary):
                    bitplane[idx][y][x] = int(c)
    return bitplane

def pbc_to_cgc(block):
    pass

def cgc_to_pbc(block):
    pass

def count_bitplane_complexity(bitplane):
    width = len(bitplane[0])
    height = len(bitplane)
    k = 0
    n = (height - 1) * width + (width - 1) * height
    for x in range(width-1):
        for y in range(height-1):
                if bitplane[y][x] != bitplane[y+1][x]:
                    k+=1
                if bitplane[y][x] != bitplane[y][x+1]:
                    k+=1
    return k/n

def message_bin_to_blocks(message):
    pass

def conjugate_blocks(block, conjugator):
    pass

