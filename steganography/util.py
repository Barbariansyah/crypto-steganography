from pathlib import Path
import os
import struct

root_path = Path('./')

''' Common Utility '''
def seed_generator(key):
    seed = 0
    for c in key:
        seed += ord(c)
    return seed

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

def float_to_binary(float_input):
    return bin(struct.unpack('!I', struct.pack('!f', float_input))[0])[2:].zfill(32)

def binary_to_float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

def image_metadata_to_binary(method, encrypt, sequential, seed, threshold, file_name):
    metadata_binary = ''
    metadata_binary += '0' if method == 'lsb' else '1'
    metadata_binary += '0' if encrypt == False else '1'
    metadata_binary += '0' if sequential == False else '1'
    metadata_binary += format(seed, '08b')
    
    file_name_binary = ''.join(format(ord(c), '08b') for c in file_name)
    metadata_binary += format(len(file_name_binary), '016b')
    metadata_binary += file_name_binary
    return metadata_binary

        