from PIL import Image
from pathlib import Path
from steganography.util import seed_generator, calculate_image_capacity, get_file_size, image_metadata_to_binary

resource_path = Path('././')
destination_path = Path('././steganography/sample-result')

'''
pixel contains r, g, b, a value in integer
'''

def embed_to_image_lsb():
    pass

def embed_to_image_bpcs():
    pass

def embed_to_image(embedded_file: str, cover_file: str, key: str, method: str, encrypt: bool, sequential: bool, threshold: bool = 0.3):  
    embedded_file_size = get_file_size(embedded_file)
    
    with Image.open(resource_path/cover_file) as img:
        width, height = img.size
        cover_capacity_bit, cover_capacity_byte = calculate_image_capacity(width, height)
        
        if(embedded_file_size > cover_capacity_byte):
            return 'embedded file size is too big for cover capacity'
        else:
            if(method=='lsb'):
                embed_to_image_lsb()
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