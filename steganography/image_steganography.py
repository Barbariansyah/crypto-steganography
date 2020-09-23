from PIL import Image
from pathlib import Path
from steganography.util import seed_generator, calculate_image_capacity, get_file_size, image_metadata_to_binary, get_file_name_from_path, bytes_to_bit
from steganography.cipher.vigenere import extended_vigenere_encrypter

resource_path = Path('./')
destination_path = Path('./steganography/sample_result')

'''
pixel contains r, g, b, a value in integer
'''

def embed_to_image_lsb(embedded_file: str, cover_img: str, key: str, encrypt: bool, sequential: bool, metadata_binary: str):
    width, height = cover_img.size
    
    if(encrypt):
        print('encrypting')
    
    if(sequential):
        print('embedding sequentially')
        for x in range(0, width):
            for y in range(0, height):
                pix = cover_img.getpixel((x,y))
                pix = list(pix)
                pix[-1] = 100
                cover_img.putpixel((x,y), tuple(pix))
        cover_img.save(destination_path/"test-new.png", "PNG")
    else:
        print('embedding randomly')
        seed = seed_generator(key)

def embed_to_image_bpcs():
    pass

def embed_to_image(embedded_file: str, cover_file: str, key: str, method: str, encrypt: bool, sequential: bool, threshold: bool = 0.3):  
    embedded_file_size = get_file_size(embedded_file)
    file_name = get_file_name_from_path(embedded_file)
    metadata_binary = image_metadata_to_binary(method, encrypt, sequential, threshold, embedded_file_size, file_name)
    with Image.open(resource_path/cover_file) as cover_img:
        width, height = cover_img.size
        cover_capacity_bit, cover_capacity_byte = calculate_image_capacity(width, height)
        
        if(embedded_file_size + len(metadata_binary) // 8 + 1 > cover_capacity_byte):
            print('embedded file size is too big for cover capacity')
            return False
        else:
            print('embedding file')
            if(method=='lsb'):
                embed_to_image_lsb(embedded_file, cover_img, key, encrypt, sequential, metadata_binary)
            else:
                embed_to_image_bpcs()


def extract_from_image():
    with Image.open(resource_path/"small-shorthair.png") as img:
        width, height = img.size
        # for x in range(0, width):
        #     for y in range(0, height):
        pix = img.getpixel((100,100))
        pix = list(pix)
        print(pix[3])
        # for p in pix:
        #     binary = format(p, '08b')
        #     print(binary)
        #     print(int(binary, 2))