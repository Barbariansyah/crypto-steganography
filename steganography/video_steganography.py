import cv2
import numpy as np
from typing import Tuple
from steganography.util import get_file_name_from_path, random_unique_location, seed_generator, bytes_to_bit, bit_to_bytes
from steganography.cipher.vigenere import extended_vigenere_encrypter, extended_vigenere_decrypter
from steganography.helper.video_helper import open_video_file


def embed_to_video(embedded_file: str, cover_video: str, key: str, encrypt: bool, sequential_bytes: bool, sequential_frames: bool) -> Tuple[bytes, tuple]:
    # Load embedded file
    with open(embedded_file, 'rb') as f:
    file_bytes = f.read()
    file_size = len(file_bytes)

    # Extract frames from cover_video
    original_video_frames = open_video_file(cover_video)

    pass


def extract_from_video(stego_video: str, key: str) -> Tuple[bytes, str]:
    pass


def save_video(content: bytes, params: tuple, path: str):
    pass
