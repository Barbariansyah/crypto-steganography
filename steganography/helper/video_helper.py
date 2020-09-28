from steganography.util import string_to_binary, binary_to_int, binary_to_string
import numpy as np
import cv2
from typing import Tuple


def open_video_file(filename: str) -> Tuple[np.array, list]:
    cap = cv2.VideoCapture(filename)
    if cap.isOpened() == False:
        raise Exception('Video file not found')

    frames = []
    params = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
        else:
            break

    params.append(int(cap.get(4)))  # width
    params.append(int(cap.get(3)))  # height
    params.append(cap.get(5))  # fps
    params.append(int(cap.get(7)))  # frame count

    cap.release()  # release video capture

    return np.array(frames), params


def video_metadata_to_binary(encrypt: bool, sequential_bytes: bool, sequential_frames: bool, file_size: int, file_name: str) -> str:
    metadata_binary = ''
    metadata_binary += '0' if encrypt == False else '1'
    metadata_binary += '0' if sequential_bytes == False else '1'
    metadata_binary += '0' if sequential_frames == False else '1'

    metadata_binary += format(file_size, '032b')
    file_name_binary = string_to_binary(file_name)
    metadata_binary += file_name_binary

    metadata_length = len(metadata_binary) + 16
    metadata_binary = format(metadata_length, '016b') + metadata_binary

    return metadata_binary


def binary_to_video_metadata(lsb_string: str) -> Tuple[int, bool, bool, bool, int, str]:
    size = binary_to_int(lsb_string[:16])

    metadata_binary = lsb_string[16:size]
    encrypt = True if metadata_binary[0] == '1' else False
    sequential_bytes = True if metadata_binary[1] == '1' else False
    sequential_frames = True if metadata_binary[2] == '1' else False

    file_size = binary_to_int(metadata_binary[3:35])
    file_name = binary_to_string(metadata_binary[35:])

    return size, encrypt, sequential_bytes, sequential_frames, file_size, file_name
