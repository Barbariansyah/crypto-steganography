from PIL import Image
from pathlib import Path

resource_path = Path('./sample-images')
destination_path = Path('./sample-result')

def embed_to_image():
    with Image.open(resource_path/"small-shorthair.png") as img:
        width, height = img.size
        for x in range(0, width):
            for y in range(0, height):
                pix = img.getpixel((x,y))
                pix = list(pix)
                pix[3] = 100
                img.putpixel((x,y), tuple(pix))
        img.save(destination_path/"test.png", "PNG")
                


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

if __name__ == "__main__":
    embed_to_image()
    # extract_from_image()