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
    cover_frames, cover_params = open_video_file(cover_video)

    file_name = get_file_name_from_path(embedded_file)
    metadata_bin = wav_helper.audio_metadata_to_binary(
        encrypt, sequential, file_size, file_name)

    embed_size = file_size * 8 + len(metadata_bin)
    if embed_size > sample_size:
        raise Exception('Embedded file size is too big for cover capacity')

    if encrypt:
        file_bytes = extended_vigenere_encrypter(file_bytes, key)
    file_bits = bytes_to_bit(file_bytes)

    return None


def extract_from_video(stego_video: str, key: str) -> Tuple[bytes, str]:
    pass


def save_video(content: bytes, params: tuple, path: str):
    pass
