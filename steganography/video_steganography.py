import cv2
import numpy as np
from typing import Tuple, List
from steganography.util import get_file_name_from_path, random_unique_location, seed_generator, bytes_to_bit, bit_to_bytes, binary_to_int
from steganography.cipher.vigenere import extended_vigenere_encrypter, extended_vigenere_decrypter
from steganography.helper.video_helper import open_video_file, video_metadata_to_binary, binary_to_video_metadata
import skvideo.io


def embed_to_video(embedded_file: str, cover_video: str, key: str, encrypt: bool, sequential_bytes: bool, sequential_frames: bool) -> Tuple[np.array, tuple]:
    # Load embedded file
    with open(embedded_file, 'rb') as f:
        file_bytes = f.read()
        file_size = len(file_bytes)

    # Extract frames from cover_video
    cover_frames, cover_params = open_video_file(cover_video)
    # Count maximum cover size
    cover_frame_width = cover_params[0]
    cover_frame_height = cover_params[1]
    cover_frame_fps = cover_params[2]
    cover_frame_count = cover_params[3]
    cover_frame_depth = 3
    cover_size = cover_frame_width * cover_frame_height * \
        cover_frame_depth * cover_frame_count

    # Create metadata
    file_name = get_file_name_from_path(embedded_file)
    metadata_bin = video_metadata_to_binary(
        encrypt, sequential_bytes, sequential_frames, file_size, file_name)

    # Check max cover size
    embed_size = file_size * 8 + len(metadata_bin)
    if embed_size > cover_size:
        raise Exception('Embedded file size is too big for cover capacity')

    # Check encrypt
    if encrypt:
        file_bytes = extended_vigenere_encrypter(file_bytes, key)
    file_bits = bytes_to_bit(file_bytes)

    # Embed metadata + content
    embedded_message = metadata_bin + file_bits

    # Embed file
    pointer = 0
    if sequential_frames:
        if sequential_bytes:
            total_length = len(embedded_message)
            for i in range(cover_frame_count):
                if pointer >= total_length:
                    break
                for j in range(cover_frame_width):
                    if pointer >= total_length:
                        break
                    for k in range(cover_frame_height):
                        if pointer >= total_length:
                            break
                        for l in range(cover_frame_depth):
                            if pointer < total_length:
                                cover_frames[i][j][k][l] = cover_frames[i][j][k][l] & ~1 | int(
                                    embedded_message[pointer])
                                pointer += 1
                            else:
                                break
        else:
            # Embedding metadata
            metadata_length = len(metadata_bin)
            for i in range(cover_frame_count):
                if pointer >= metadata_length:
                    break
                for j in range(cover_frame_width):
                    if pointer >= metadata_length:
                        break
                    for k in range(cover_frame_height):
                        if pointer >= metadata_length:
                            break
                        for l in range(cover_frame_depth):
                            if pointer < metadata_length:
                                cover_frames[i][j][k][l] = cover_frames[i][j][k][l] & ~1 | int(
                                    metadata_bin[pointer])
                                pointer += 1
                            else:
                                break

            # Max capacity frame
            max_capacity_frame = cover_frame_height * cover_frame_width * cover_frame_depth

            # Create random
            random_loc = random_unique_location(
                metadata_length, len(file_bits), seed_generator(
                    key), max_capacity_frame*((len(file_bits) // max_capacity_frame)+1))

            # Embedding message
            for idx, loc in enumerate(random_loc):
                x, rem_frame = divmod(loc, max_capacity_frame)
                y, rem = divmod(rem_frame, cover_frame_height*3)
                z, rem = divmod(rem, 3)
                i = rem
                cover_frames[x][y][z][i] = cover_frames[x][y][z][i] & ~1 | int(
                    file_bits[idx])
    else:
        if sequential_bytes:
            # Embedding metadata
            metadata_length = len(metadata_bin)
            for i in range(cover_frame_count):
                if pointer >= metadata_length:
                    break
                for j in range(cover_frame_height):
                    if pointer >= metadata_length:
                        break
                    for k in range(cover_frame_width):
                        if pointer >= metadata_length:
                            break
                        for l in range(cover_frame_depth):
                            if pointer < metadata_length:
                                cover_frames[i][j][k][l] = cover_frames[i][j][k][l] & ~1 | int(
                                    metadata_bin[pointer])
                                pointer += 1
                            else:
                                break

            # Max capacity frame
            max_capacity_frame = cover_frame_height * cover_frame_width * cover_frame_depth

            # Create random
            random_loc = random_unique_location(
                1, (len(file_bits) // max_capacity_frame)+1, seed_generator(
                    key), cover_frame_count)

            # Embedding message
            pointer = 0
            total_length = len(file_bits)
            for _, loc in enumerate(random_loc):
                for j in range(cover_frame_width):
                    if pointer >= total_length:
                        break
                    for k in range(cover_frame_height):
                        if pointer >= total_length:
                            break
                        for l in range(cover_frame_depth):
                            if pointer < total_length:
                                cover_frames[loc][j][k][l] = cover_frames[loc][j][k][l] & ~1 | int(
                                    file_bits[pointer])
                                pointer += 1
                            else:
                                break

        else:
            # Embedding metadata
            metadata_length = len(metadata_bin)
            for i in range(cover_frame_count):
                if pointer >= metadata_length:
                    break
                for j in range(cover_frame_width):
                    if pointer >= metadata_length:
                        break
                    for k in range(cover_frame_height):
                        if pointer >= metadata_length:
                            break
                        for l in range(cover_frame_depth):
                            if pointer < metadata_length:
                                cover_frames[i][j][k][l] = cover_frames[i][j][k][l] & ~1 | int(
                                    metadata_bin[pointer])
                                pointer += 1
                            else:
                                break

            # Max capacity frame
            max_capacity_frame = cover_frame_height * cover_frame_width * cover_frame_depth

            # Create random
            random_pixel_loc = random_unique_location(
                metadata_length, len(file_bits), seed_generator(key), max_capacity_frame*cover_frame_count)

            # Embedding message
            for idx, loc in enumerate(random_pixel_loc):
                x, rem_frame = divmod(loc, max_capacity_frame)
                y, rem = divmod(rem_frame, cover_frame_height*3)
                z, rem = divmod(rem, 3)
                i = rem
                cover_frames[x][y][z][i] = cover_frames[x][y][z][i] & ~1 | int(
                    file_bits[idx])

    # TODO: PSNR
    return cover_frames, cover_params, 0


def extract_from_video(stego_video: str, key: str) -> Tuple[bytes, str]:
    # Extract frames from cover_video
    cover_frames, cover_params = open_video_file(stego_video)
    cover_frame_width = cover_params[0]
    cover_frame_height = cover_params[1]
    cover_frame_count = cover_params[3]
    cover_frame_depth = 3

    # Extract LSB
    lsbs = ''
    metadata_frames = cover_frames[0]
    for i in range(cover_frame_width):
        for j in range(cover_frame_height):
            for k in range(3):
                lsbs += str(metadata_frames[i][j][k] & 1)
    size, encrypt, sequential_bytes, sequential_frames, file_size, file_name = binary_to_video_metadata(
        lsbs)

    file_size_bit = file_size * 8

    # Extract file
    file_bits = ''
    if sequential_frames:
        if sequential_bytes:
            for idx in range(file_size_bit):
                loc = size + idx
                file_bits += str(lsbs[loc])
        else:
            # Max capacity frame
            max_capacity_frame = cover_frame_height * cover_frame_width * cover_frame_depth

            # Create random
            random_loc = random_unique_location(
                size, file_size_bit, seed_generator(
                    key), max_capacity_frame*((file_size_bit // max_capacity_frame)+1))

            # Embedding message
            for idx, loc in enumerate(random_loc):
                x, rem_frame = divmod(loc, max_capacity_frame)
                y, rem = divmod(rem_frame, cover_frame_height*3)
                z, rem = divmod(rem, 3)
                i = rem
                file_bits += str(cover_frames[x][y][z][i] & 1)
    else:
        if sequential_bytes:
            # Max capacity frame
            max_capacity_frame = cover_frame_height * cover_frame_width * cover_frame_depth

            # Create random
            random_loc = random_unique_location(
                1, ((file_size_bit) // max_capacity_frame)+1, seed_generator(
                    key), cover_frame_count)

            # Embedding message
            pointer = 0
            total_length = file_size_bit
            for _, loc in enumerate(random_loc):
                for j in range(cover_frame_width):
                    if pointer >= total_length:
                        break
                    for k in range(cover_frame_height):
                        if pointer >= total_length:
                            break
                        for l in range(cover_frame_depth):
                            if pointer < total_length:
                                file_bits += str(cover_frames[loc][j][k][l] & 1)
                                pointer += 1
                            else:
                                break
        else:
            # Max capacity frame
            max_capacity_frame = cover_frame_height * cover_frame_width * cover_frame_depth

            # Create random
            random_pixel_loc = random_unique_location(
                size, file_size_bit, seed_generator(key), max_capacity_frame*cover_frame_count)

            # Embedding message
            for idx, loc in enumerate(random_pixel_loc):
                x, rem_frame = divmod(loc, max_capacity_frame)
                y, rem = divmod(rem_frame, cover_frame_height*3)
                z, rem = divmod(rem, 3)
                i = rem
                file_bits += str(cover_frames[x][y][z][i] & 1)

    file_bytes = bit_to_bytes(file_bits)

    # Decrypt if encrypted
    if encrypt:
        file_bytes = extended_vigenere_decrypter(file_bytes, key)

    return file_bytes, file_name


def save_video(content: List[np.array], params: tuple, path: str):
    cover_frame_width = params[0]
    cover_frame_height = params[1]
    cover_frame_fps = params[2]

    writer = skvideo.io.FFmpegWriter(path, outputdict={
        '-vcodec': 'ffv1',  # use the h.264 codec
        '-crf': '0',  # set the constant rate factor to 0, which is lossless
        '-preset': 'veryslow'
    })

    for frame in content:
        writer.writeFrame(frame[:, :, ::-1])

    writer.close()


def play_video(filename: str):
    cap = cv2.VideoCapture(filename)

    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:

            cv2.imshow('Frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        else:
            break

    cap.release()
