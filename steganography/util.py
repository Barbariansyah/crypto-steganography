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

def image_metadata_to_binary(method, encrypt, sequential, threshold, file_size, file_name):
    metadata_binary = ''
    metadata_binary += '0' if method == 'lsb' else '1'
    metadata_binary += '0' if encrypt == False else '1'
    metadata_binary += '0' if sequential == False else '1'
    metadata_binary += float_to_binary(threshold)
    metadata_binary += format(file_size, '032b')
    file_name_binary = string_to_binary(file_name)
    metadata_binary += format(len(file_name_binary), '016b')
    metadata_binary += file_name_binary
    return metadata_binary

        