from PIL import Image
from pathlib import Path
from steganography.util import *
from steganography.cipher.vigenere import extended_vigenere_encrypter, extended_vigenere_decrypter
import math

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
        cover_img.save(destination_path/get_file_name_from_path(cover_img.filename))
    else:
        metadata_length = len(metadata_binary)
        print('embedding randomly')
        seed = seed_generator(key)
        location = random_unique_location(metadata_length, len(content), seed, width*height*3)
        
        #embedding metadata
        for x in range(0, width):
            if pointer >= metadata_length:
                break
            for y in range(0, height):
                if pointer >= metadata_length:
                    break
                pix = cover_img.getpixel((x,y))
                pix = list(pix)
                for i in range(3):
                    if pointer < metadata_length:
                        pix[i] = pix[i] & ~1 | int(metadata_binary[pointer])
                        pointer += 1
                    else:
                        break
                cover_img.putpixel((x,y), tuple(pix))

        #embedding content
        for idx, loc in enumerate(location):
            x, rem = divmod(loc, height*3) 
            y, rem = divmod(rem, 3)
            i = rem
            pix = cover_img.getpixel((x,y))
            pix = list(pix)
            pix[i] = pix[i] & ~1 | int(content[idx])
            cover_img.putpixel((x,y), tuple(pix))
        
        cover_img.save(destination_path/get_file_name_from_path(cover_img.filename))
                

def embed_to_image_bpcs(embedded_file, cover_img, key, encrypt, sequential, threshold, metadata_binary):
    width, height = cover_img.size
    cover_img_filename = cover_img.filename

    cover_img = cover_img.convert('RGB')
    
    with open(embedded_file, 'rb') as f:
        content = f.read()
    
    if(encrypt):
        content = extended_vigenere_encrypter(content, key)
    
    content = bytes_to_bit(content)
    print(len(content))

    blocks = cover_to_blocks(cover_img)
    blocks_width, blocks_height = len(blocks[0]), len(blocks)

    #change blocks to blocks of bitplane
    for y in range(len(blocks)):
        for x in range(len(blocks[y])):
                blocks[y][x] = block_to_bitplane(blocks[y][x])

    message_blocks = message_bin_to_blocks(message=content)
    conjugation_map = generate_conjugation_map(message_blocks, threshold)

    #insert additional metadata
    metadata_conjugation_map = ''.join(str(m) for m in conjugation_map)
    metadata_binary += format(len(metadata_conjugation_map), '032b')
    metadata_binary += metadata_conjugation_map

    #embedding metadata
    metadata_length = len(metadata_binary)
    
    width_start = math.ceil(math.ceil(math.ceil(metadata_length / 3) / height) / 8)

    message_pointer = 0
    if(sequential):
        # inserting message into bitplane
        for x in range(width_start, blocks_width):
            if message_pointer >= len(message_blocks):
                break
            for y in range(0, blocks_height):
                if message_pointer >= len(message_blocks):
                    break
                for i in range(0, 24):
                    if message_pointer < len(message_blocks):
                        if count_bitplane_complexity(blocks[y][x][i]) > threshold:
                            blocks[y][x][i] = message_blocks[message_pointer]
                            message_pointer+=1
                        else:
                            continue
                    else:
                        break
    else:
        print('embedding randomly')

    stego_blocks = [[None for _ in range(blocks_width)] for _ in range(blocks_height)]
    for x in range(blocks_width):
        for y in range(blocks_height):
            stego_blocks[y][x] = bitplane_to_block(blocks[y][x])
    
    stego_img = blocks_to_np_img_array(stego_blocks, width, height)
    stego_img = Image.fromarray(stego_img).convert('RGB')
    pointer = 0
    for x in range(0, width):
        if pointer >= metadata_length:
            break
        for y in range(0, height):
            if pointer >= metadata_length:
                break
            pix = stego_img.getpixel((x,y))
            pix = list(pix)
            for i in range(3):
                if pointer < metadata_length:
                    pix[i] = pix[i] & ~1 | int(metadata_binary[pointer])
                    pointer += 1
                else:
                    break
            stego_img.putpixel((x,y), tuple(pix))
    
    # # stego_img.show()
    # return stego_img.tobytes()
    stego_img.save(destination_path/get_file_name_from_path(cover_img_filename))

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
                embed_to_image_bpcs(embedded_file, cover_img, key, encrypt, sequential, threshold, metadata_binary)


def extract_from_image_lsb(binary, metadata_size, encrypt, sequential, embed_file_size, embed_file_name, key, cover_width, cover_height):
    if sequential :
        print('extracting seq')
        content_binary = binary[metadata_size:metadata_size+embed_file_size*8]
    else:
        print('extracting random')
        location = random_unique_location(metadata_size, embed_file_size*8, seed_generator(key), cover_width*cover_height*3)
        content_binary = ''
        for loc in location:
            content_binary += binary[loc]
    content_bytes = bit_to_bytes(content_binary)
    if(encrypt):
        content_bytes = extended_vigenere_decrypter(content_bytes, key)
    with open(destination_path/embed_file_name, 'wb+') as f:
        f.write(content_bytes)


def extract_from_image_bpcs(stego_img, metadata_size, encrypt, sequential, embed_file_size, embed_file_name, key, width, height, conjugation_map, threshold):
    width_start = math.ceil(math.ceil(math.ceil(metadata_size / 3) / height) / 8)
    blocks = cover_to_blocks(stego_img)
    blocks_width, blocks_height = len(blocks[0]), len(blocks)
    #change blocks to blocks of bitplane
    for y in range(len(blocks)):
        for x in range(len(blocks[y])):
                blocks[y][x] = block_to_bitplane(blocks[y][x])
    message_blocks = []
    message_blocks_pointer = 0
    message_blocks_length = math.ceil(embed_file_size * 8 / 64)
    if(sequential):
        print('extracting seq')
        for x in range(width_start, blocks_width):
            if message_blocks_pointer >= message_blocks_length:
                break
            for y in range(0, blocks_height):
                if message_blocks_pointer >= message_blocks_length:
                    break
                for i in range(0,24):
                    if message_blocks_pointer < message_blocks_length:
                        if count_bitplane_complexity(blocks[y][x][i]) > threshold:
                            message_blocks.append(blocks[y][x][i])
                            message_blocks_pointer+=1
                        else:
                            continue
                    else:
                        break
        message_bin = message_blocks_to_bin(message_blocks, conjugation_map, embed_file_size * 8)
    else:
        print('extracting random')
    content_bytes = bit_to_bytes(message_bin)
    if(encrypt):
        content_bytes = extended_vigenere_decrypter(content_bytes, key)
    with open(destination_path/embed_file_name, 'wb+') as f:
        f.write(content_bytes)

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
    if(method=='lsb'):
        extract_from_image_lsb(binary, metadata_size, encrypt, sequential, embed_file_size, embed_file_name, key, width, height)
    else:
        conjugation_map_length = binary_to_int(binary[metadata_size:metadata_size+32])
        conjugation_map = [ int(i) for i in binary[metadata_size+32:metadata_size+32+conjugation_map_length] ]
        extract_from_image_bpcs(stego_img, metadata_size+32+conjugation_map_length, encrypt, sequential, embed_file_size, embed_file_name, key, width, height, conjugation_map, threshold)
