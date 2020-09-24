from pathlib import Path
import os
import struct
from bitarray import bitarray
import random

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