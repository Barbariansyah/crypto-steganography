from PIL import Image
from typing import Tuple, List
from io import BytesIO
from steganography.util import *
from steganography.cipher.vigenere import extended_vigenere_encrypter, extended_vigenere_decrypter
import math

def embed_to_image_lsb(embedded_file: str, cover_img: Image.Image, key: str, encrypt: bool, sequential: bool, metadata_binary: str) -> Tuple[bytes, Image.Image]:
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
    else:
        metadata_length = len(metadata_binary)
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
    
    with BytesIO() as output:
        cover_img.save(output, 'BMP')
        cover_img_bytes = output.getvalue()

    return cover_img_bytes, cover_img
                
def embed_to_image_bpcs(embedded_file: str, cover_img: Image.Image, key: str, encrypt: bool, sequential: bool, threshold: float, metadata_binary: str) -> Tuple[bytes, Image.Image]:
    width, height = cover_img.size
    cover_img_filename = cover_img.filename

    cover_img = cover_img.convert('RGB')
    
    with open(embedded_file, 'rb') as f:
        content = f.read()
    
    if(encrypt):
        content = extended_vigenere_encrypter(content, key)
    
    content = bytes_to_bit(content)

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
        seed = seed_generator(key)
        random.seed(seed)
        locations = random.sample(range(0, len(message_blocks)), len(message_blocks))
        for x in range(width_start, blocks_width):
            if message_pointer >= len(message_blocks):
                break
            for y in range(0, blocks_height):
                if message_pointer >= len(message_blocks):
                    break
                for i in range(0, 24):
                    if message_pointer < len(message_blocks):
                        if count_bitplane_complexity(blocks[y][x][i]) > threshold:
                            blocks[y][x][i] = message_blocks[locations[message_pointer]]
                            message_pointer+=1
                        else:
                            continue
                    else:
                        break

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
    
    with BytesIO() as output:
        stego_img.save(output, 'BMP')
        stego_img_bytes = output.getvalue()

    return stego_img_bytes, stego_img

def embed_to_image(embedded_file: str, cover_file: str, key: str, method: str, encrypt: bool, sequential: bool, threshold: float = 0.3) -> Tuple[bytes, Image.Image, float]:  
    embedded_file_size = get_file_size(embedded_file)
    embedded_file_name = get_file_name_from_path(embedded_file)
    metadata_binary = image_metadata_to_binary(method, encrypt, sequential, threshold, embedded_file_size, embedded_file_name)
    with Image.open(cover_file) as cover_img:
        original = cover_img.copy()
        cover_capacity_bit, cover_capacity_byte = calculate_image_capacity(cover_img, method, threshold)
        if(embedded_file_size + len(metadata_binary) // 8 + 1 > cover_capacity_byte):
            raise Exception('embedded file size is too big for cover capacity')
        else:
            if(method=='lsb'):
                stego_img_bytes, stego_img = embed_to_image_lsb(embedded_file, cover_img, key, encrypt, sequential, metadata_binary)
            else:
                stego_img_bytes, stego_img = embed_to_image_bpcs(embedded_file, cover_img, key, encrypt, sequential, threshold, metadata_binary)
        psnr = calculate_psnr(original, stego_img)
    return stego_img_bytes, stego_img, psnr

def extract_from_image_lsb(binary: str, metadata_size: int, encrypt: bool, sequential: bool, embed_file_size: int, key: str, cover_width: int, cover_height: int) -> bytes:
    if sequential :
        content_binary = binary[metadata_size:metadata_size+embed_file_size*8]
    else:
        location = random_unique_location(metadata_size, embed_file_size*8, seed_generator(key), cover_width*cover_height*3)
        content_binary = ''
        for loc in location:
            content_binary += binary[loc]
    content_bytes = bit_to_bytes(content_binary)
    if(encrypt):
        content_bytes = extended_vigenere_decrypter(content_bytes, key)
    return content_bytes

def extract_from_image_bpcs(stego_img: Image.Image, metadata_size: int, encrypt: bool, sequential: bool, embed_file_size: int, key: str, width: int, height: int, conjugation_map: List[int], threshold: float = 0.3) -> bytes:
    width_start = math.ceil(math.ceil(math.ceil(metadata_size / 3) / height) / 8)
    blocks = cover_to_blocks(stego_img)
    blocks_width, blocks_height = len(blocks[0]), len(blocks)
    #change blocks to blocks of bitplane
    for y in range(len(blocks)):
        for x in range(len(blocks[y])):
                blocks[y][x] = block_to_bitplane(blocks[y][x])
    message_blocks_pointer = 0
    message_blocks_length = math.ceil(embed_file_size * 8 / 64)
    message_blocks = [None for _ in range(message_blocks_length)]
    if(sequential):
        for x in range(width_start, blocks_width):
            if message_blocks_pointer >= message_blocks_length:
                break
            for y in range(0, blocks_height):
                if message_blocks_pointer >= message_blocks_length:
                    break
                for i in range(0,24):
                    if message_blocks_pointer < message_blocks_length:
                        if count_bitplane_complexity(blocks[y][x][i]) > threshold:
                            message_blocks[message_blocks_pointer] = blocks[y][x][i]
                            message_blocks_pointer+=1
                        else:
                            continue
                    else:
                        break
        message_bin = message_blocks_to_bin(message_blocks, conjugation_map, embed_file_size * 8)
    else:
        seed = seed_generator(key)
        random.seed(seed)
        locations = random.sample(range(0, message_blocks_length), message_blocks_length)
        for x in range(width_start, blocks_width):
            if message_blocks_pointer >= message_blocks_length:
                break
            for y in range(0, blocks_height):
                if message_blocks_pointer >= message_blocks_length:
                    break
                for i in range(0,24):
                    if message_blocks_pointer < message_blocks_length:
                        if count_bitplane_complexity(blocks[y][x][i]) > threshold:
                            message_blocks[locations[message_blocks_pointer]] = blocks[y][x][i]
                            message_blocks_pointer+=1
                        else:
                            continue
                    else:
                        break
        message_bin = message_blocks_to_bin(message_blocks, conjugation_map, embed_file_size * 8)

    content_bytes = bit_to_bytes(message_bin)
    if(encrypt):
        content_bytes = extended_vigenere_decrypter(content_bytes, key)
    return content_bytes

def extract_from_image(stego_file: str, key: str) -> Tuple[bytes, str]:
    binary = ''
    with Image.open(stego_file) as stego_img:
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
        content_bytes = extract_from_image_lsb(binary, metadata_size, encrypt, sequential, embed_file_size, key, width, height)
    else:
        conjugation_map_length = binary_to_int(binary[metadata_size:metadata_size+32])
        conjugation_map = [ int(i) for i in binary[metadata_size+32:metadata_size+32+conjugation_map_length] ]
        content_bytes = extract_from_image_bpcs(stego_img, metadata_size+32+conjugation_map_length, encrypt, sequential, embed_file_size, key, width, height, conjugation_map, threshold)
    return content_bytes, embed_file_name

def calculate_psnr(cover_img: Image.Image, stego_img: Image.Image) -> float:
    width, height = cover_img.size
    r_se, g_se, b_se = 0, 0, 0
    for x in range(0, width):
        for y in range(0, height):
            s_pix = stego_img.getpixel((x,y))
            s_pix = list(s_pix)
            c_pix = cover_img.getpixel((x,y))
            c_pix = list(c_pix)
            r_se += (s_pix[0] - c_pix[0]) ** 2
            g_se += (s_pix[1] - c_pix[1]) ** 2
            b_se += (s_pix[2] - c_pix[2]) ** 2
    r_mse = r_se / (width * height)
    g_mse = g_se / (width * height)
    b_mse = b_se / (width * height)
    mse = (r_mse + g_mse + b_mse) / 3
    psnr = 10 * math.log(((255 ** 2) / mse), 10)
    return psnr

def save_image(image: Image.Image, path: str):
    image.save(path)