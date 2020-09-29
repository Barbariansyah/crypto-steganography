from bitarray import bitarray
import numpy as np
import os
import struct
import random
import math

''' Common Utility '''
def seed_generator(key):
    seed = 0
    for c in key:
        seed += ord(c)
    return seed

def random_unique_location(metadata_length, content_length, seed, cover_size):
    random.seed(seed)
    location = random.sample(range(metadata_length, cover_size), content_length)
    return location    

def bytes_to_bit(bytes_input):
    temp = bitarray()
    temp.frombytes(bytes_input)
    return temp.to01()

def bit_to_bytes(bit_input):
    temp = bitarray(bit_input)
    return temp.tobytes()

def calculate_image_capacity(cover_img, method, threshold = 0.3):
    if method == 'lsb':
        width, height = cover_img.size
        bit_capacity = width * height * 3
        byte_capacity = bit_capacity // 8
    else:
        cover_img_conv = cover_img.convert('RGB')

        blocks = cover_to_blocks(cover_img_conv)
        blocks_width, blocks_height = len(blocks[0]), len(blocks)
        for x in range(blocks_width):
            for y in range(blocks_height):
                    blocks[y][x] = block_to_bitplane(blocks[y][x])
        blocks_depth = len(blocks[0][0])

        bit_capacity = 0
        for x in range(blocks_width):
            for y in range(blocks_height):
                for i in range(blocks_depth):
                    if count_bitplane_complexity(blocks[y][x][i]) > threshold:
                        bit_capacity += 64 
        byte_capacity = bit_capacity // 8

    return bit_capacity, byte_capacity

def get_file_size(file_name):
    return os.stat(file_name).st_size

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
    _, file_name = os.path.split(path)
    return file_name

def save_bytes_to_file(file_bytes: bytes, path: str):
    with open(path, 'wb+') as f:
        f.write(file_bytes)

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
    if width % 8 != 0:
        rem = 8 - width % 8
        width += rem
        for i in range(height):
            pixels[i].extend([(255, 255, 255) for _ in range(rem)])
    if height % 8 != 0:
        rem = 8 - height % 8
        height += rem
        for i in range(rem):
            pixels.append([(255, 255, 255) for _ in range(width)])

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
            r, g, b = block[y][x]
            pixel_binary = int_to_binary(r) + int_to_binary(g) + int_to_binary(b)
            for idx, c in enumerate(pixel_binary):
                    bitplane[idx][y][x] = int(c)
    return bitplane

def bitplane_to_block(bitplane, depth = 3):
    block = [[[0 for _ in range(depth)] for _ in range(8)] for _ in range(8)]
    for x in range(8):
        for y in range(8):
            pixel_binary = ''
            for idx in range(8 * depth):
                pixel_binary += str(bitplane[idx][y][x])
            for idx in range(depth):
                curr_pixel_binary = pixel_binary[idx*8:(idx+1)*8]
                block[y][x][idx] = binary_to_int(curr_pixel_binary)
    return block

def blocks_to_np_img_array(blocks, width, height, depth = 3):
    img_array = [[[0 for _ in range(depth)] for _ in range(width)] for _ in range(height)]
    for x in range(width):
        for y in range(height):
            blocks_x, idx_x = x // 8, x % 8
            blocks_y, idx_y = y // 8, y % 8
            for i in range(depth):
                img_array[y][x][i] = blocks[blocks_y][blocks_x][idx_y][idx_x][i]
    return np.array(img_array, dtype='uint8')

def bitplane_pbc_to_cgc(bitplane):
    width = len(bitplane[0])
    height = len(bitplane)
    cgc = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        cgc[y][0] = bitplane[y][0]
        for x in range(1, width):    
            cgc[y][x] = bitplane[y][x] ^ bitplane[y][x-1]
    return cgc

def bitplane_cgc_to_pbc(bitplane):
    width = len(bitplane[0])
    height = len(bitplane)
    pbc = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        pbc[y][0] = bitplane[y][0]
        for x in range(1, width):    
            pbc[y][x] = bitplane[y][x] ^ pbc[y][x-1]
    return pbc

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
    if len(message) % 64 != 0:
        message += (64 - len(message) % 64) * '0'
    blocks = []
    for i in range(0, len(message), 64):
        cur_bin = [int(c) for c in message[i:i+64]]
        temp = np.reshape(cur_bin, (8, 8)).T
        temp = temp.tolist()
        blocks.append(temp)
    return blocks

def message_blocks_to_bin(message_blocks, conjugation_map, message_length):
    message = ''
    for i, block in enumerate(message_blocks):
        if conjugation_map[i]==1:
            temp = conjugate_block_with_wc(block)
        else:
            temp = block
        temp = np.array(temp).T
        temp = np.reshape(temp, (64))
        message += ''.join(str(b) for b in temp)
    return message[:message_length]

def conjugate_block_with_wc(block):
    conjugator = [
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
        [0,1,0,1,0,1,0,1],
        [1,0,1,0,1,0,1,0],
    ]
    for x in range(8):
        for y in range(8):
            conjugator[y][x] = conjugator[y][x] ^ block[y][x]
    return conjugator
            

def generate_conjugation_map(message_blocks, threshold):
    conjugation_map = [0 for _ in range(len(message_blocks))]
    for idx, block in enumerate(message_blocks):
        if count_bitplane_complexity(block) < threshold:
            conjugation_map[idx] = 1
            message_blocks[idx] = conjugate_block_with_wc(block)
    return conjugation_map
