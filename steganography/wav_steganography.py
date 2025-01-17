import wave
import math
import subprocess
from typing import Tuple
from copy import deepcopy
from steganography.helper import wav_helper
from steganography.util import get_file_name_from_path, random_unique_location, seed_generator, bytes_to_bit, bit_to_bytes
from steganography.cipher.vigenere import extended_vigenere_encrypter, extended_vigenere_decrypter


def embed_to_audio(embedded_file: str, cover_audio: str, key: str, encrypt: bool, sequential: bool) -> Tuple[bytes, tuple]:
    # Load files and do checks
    with open(embedded_file, 'rb') as f:
        file_bytes = f.read()
        file_size = len(file_bytes)

    with wave.open(cover_audio, 'rb') as w:
        frame_count = w.getnframes()
        sample_params = w.getparams()
        samples = [b for b in w.readframes(frame_count)]
        sample_size = len(samples)
        samples_og = deepcopy(samples)

    file_name = get_file_name_from_path(embedded_file)
    metadata_bin = wav_helper.audio_metadata_to_binary(
        encrypt, sequential, file_size, file_name)

    embed_size = file_size * 8 + len(metadata_bin)
    if embed_size > sample_size:
        raise Exception('Embedded file size is too big for cover capacity')

    if encrypt:
        file_bytes = extended_vigenere_encrypter(file_bytes, key)
    file_bits = bytes_to_bit(file_bytes)

    # Embed metadata
    for idx, bit in enumerate(metadata_bin):
        ibit = int(bit)
        samples[idx] = (samples[idx] & ~1) | ibit

    # Embed file
    if sequential:
        for idx, bit in enumerate(file_bits):
            loc = len(metadata_bin) + idx
            ibit = int(bit)
            samples[loc] = (samples[loc] & ~1) | ibit
    else:
        random_loc = random_unique_location(
            len(metadata_bin), file_size * 8, seed_generator(key), sample_size)
        for idx, bit in enumerate(file_bits):
            loc = random_loc[idx]
            ibit = int(bit)
            samples[loc] = (samples[loc] & ~1) | ibit

    psnr = calculate_psnr(samples_og, samples)
    return bytes(samples), sample_params, psnr


def extract_from_audio(stego_audio: str, key: str) -> Tuple[bytes, str]:
    # Load files and do checks
    with wave.open(stego_audio, 'rb') as w:
        frame_size = w.getnframes()
        stego_samples = [b for b in w.readframes(frame_size)]
        sample_size = len(stego_samples)

    # Extract lsb
    lsbs = ''
    for sample in stego_samples:
        lsbs += str(sample & 1)

    # Deserialize metadata
    metadata_size, encrypt, sequential, file_size, file_name = wav_helper.binary_to_audio_metadata(
        lsbs)
    file_size_bit = file_size * 8

    # Extract file
    file_bits = ''
    if sequential:
        for idx in range(file_size_bit):
            loc = metadata_size + idx
            file_bits += str(lsbs[loc])
    else:
        random_loc = random_unique_location(
            metadata_size, file_size_bit, seed_generator(key), sample_size)
        for loc in random_loc:
            file_bits += str(lsbs[loc])
    file_bytes = bit_to_bytes(file_bits)

    # Decrypt if encrypted
    if encrypt:
        file_bytes = extended_vigenere_decrypter(file_bytes, key)

    return file_bytes, file_name


def save_audio(content: bytes, params: tuple, path: str):
    with wave.open(path, 'wb') as n:
        n.setparams(params)
        n.writeframes(content)


def play_audio(path: str):
    try:
        command = ['vlc', f'file://{path}']
        subprocess.run(command)
    except FileNotFoundError:
        raise Exception('Cannot play audio, VLC is required')
    except:
        raise Exception('Cannot play audio')


def calculate_psnr(original_bytes: list, stego_bytes: list) -> float:
    sse = 0
    for og_byte, stego_byte in zip(original_bytes, stego_bytes):
        sse += (og_byte - stego_byte) ** 2
    rms = (sse / len(original_bytes)) ** (1/2)
    psnr = 20 * math.log10(255 / rms)
    return psnr
