from steganography.cipher.vigenere import extended_vigenere_encrypter
from steganography.image_steganography.lsb import *
from steganography.util import *

if __name__ == "__main__":
    embed_to_image(embedded_file="steganography/sample_images/small-kanye.png", cover_file="steganography/sample_images/shorthair.png", key="steganography", method="lsb", encrypt=True, sequential=True)