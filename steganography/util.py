from pathlib import Path
import os

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
    # print(root_path/file_name)
    # return(root_path)