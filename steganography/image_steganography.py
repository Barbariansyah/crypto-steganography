from PIL import Image
from pathlib import Path
from steganography.util import seed_generator, calculate_image_capacity, get_file_size, image_metadata_to_binary, get_file_name_from_path, bytes_to_bit, binary_to_image_metadata, binary_to_int, bit_to_bytes
from steganography.cipher.vigenere import extended_vigenere_encrypter, extended_vigenere_decrypter

resource_path = Path('./')
destination_path = Path('./steganography/sample_result')

'''
pixel contains r, g, b, a value in integer
'''

def embed_to_image_lsb(embedded_file: str, cover_img, key: str, encrypt: bool, sequential: bool, metadata_binary: str):
    width, height = cover_img.size
    with open(embedded_file, 'rb') as f:
        content = f.read()
    
    if(encrypt):
        content = extended_vigenere_encrypter(content, key)
    
    content = bytes_to_bit(content)
    
    pointer = 0
    embedded_message = metadata_binary + content
    total_length = len(embedded_message)
    if(sequential):
        print('embedding sequentially')
        for x in range(0, width):
            if pointer >= total_length:
                break
            for y in range(0, height):
                if pointer >= total_length:
                    break
                pix = cover_img.getpixel((x,y))
                pix = list(pix)
                for i in range(3):
                    if pointer < total_length:
                        pix[i] = pix[i] & ~1 | int(embedded_message[pointer])
                        pointer += 1
                    else:
                        break
                cover_img.putpixel((x,y), tuple(pix))
        cover_img.save(destination_path/get_file_name_from_path(cover_img.filename), "PNG")
    else:
        print('embedding randomly')
        seed = seed_generator(key)

def embed_to_image_bpcs():
    pass

def embed_to_image(embedded_file: str, cover_file: str, key: str, method: str, encrypt: bool, sequential: bool, threshold: bool = 0.3):  
    embedded_file_size = get_file_size(embedded_file)
    embedded_file_name = get_file_name_from_path(embedded_file)
    metadata_binary = image_metadata_to_binary(method, encrypt, sequential, threshold, embedded_file_size, embedded_file_name)
    with Image.open(resource_path/cover_file) as cover_img:
        width, height = cover_img.size
        cover_capacity_bit, cover_capacity_byte = calculate_image_capacity(width, height)
        print(cover_img.filename)
        if(embedded_file_size + len(metadata_binary) // 8 + 1 > cover_capacity_byte):
            print('embedded file size is too big for cover capacity')
            return False
        else:
            print('embedding file')
            if(method=='lsb'):
                embed_to_image_lsb(embedded_file, cover_img, key, encrypt, sequential, metadata_binary)
            else:
                embed_to_image_bpcs()


def extract_from_image_lsb(binary, metadata_size, encrypt, sequential, embed_file_size, embed_file_name, key):
    content_binary = binary[metadata_size:metadata_size+embed_file_size*8]
    print(content_binary)
    if sequential :
        content_bytes = bit_to_bytes(content_binary)
        if(encrypt):
            content_bytes = extended_vigenere_decrypter(content_bytes, key)
        with open(destination_path/embed_file_name, 'wb+') as f:
            f.write(content_bytes)

def extract_from_image_bpcs():
    pass

def extract_from_image(stego_file: str, key: str):
    binary = ''
    with Image.open(resource_path/stego_file) as stego_img:
        width, height = stego_img.size
        for x in range(0, width):
            for y in range(0, height):
                pix = stego_img.getpixel((x,y))
                pix = list(pix)
                for i in range(3):
                        binary += str(pix[i] & 1)
    metadata_size = binary_to_int(binary[:16])
    metadata_size, method, encrypt, sequential, threshold, embed_file_size, embed_file_name = binary_to_image_metadata(binary[:metadata_size])
    print(metadata_size)
    print(method)
    print(encrypt)
    print(sequential)
    print(threshold)
    print(embed_file_size)
    print(embed_file_name)
    if(method=='lsb'):
        extract_from_image_lsb(binary, metadata_size, encrypt, sequential, embed_file_size, embed_file_name, key)
    else:
        return
        # extract_from_image_bpcs()
