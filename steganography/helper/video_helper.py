from steganography.util import string_to_binary, binary_to_int, binary_to_string
import numpy as np
import ffmpeg
import os
import uuid
import shutil
import subprocess
from PIL import Image
from typing import Tuple


def open_video_file(mode: str, filename: str):
    # Open video file and save as array of image
    audio_path = 'steganography/sample_video_audio/test.aac'
    if mode == 'embed':
        # Get framerate
        command = ['ffprobe',
                   '-v', 'error',
                   '-select_streams', 'v:0',
                   '-show_entries', 'stream=r_frame_rate',
                   '-of', 'csv=s=x:p=0',
                   filename]
        cmd_out, cmd_error = subprocess.Popen(
            command, stdout=subprocess.PIPE).communicate()
        cmd_out = cmd_out.decode()
        frame_speed, divisor = cmd_out.split("/")
        framerate = int(frame_speed) / int(divisor)

        # Check and extract audio
        command = ['ffprobe',
                   '-i', filename,
                   '-show_streams',
                   '-select_streams', 'a',
                   '-loglevel', 'error'
                   ]
        cmd_out, cmd_error = subprocess.Popen(
            command, stdout=subprocess.PIPE).communicate()

        # Extract audio
        if len(cmd_out) != 0:
            command = ['ffmpeg',
                       '-i', filename,
                       '-y',
                       audio_path]
            retcode = subprocess.call(command)

    # Get video size
    command = ['ffprobe',
               '-v', 'error',
               '-select_streams', 'v:0',
               '-show_entries', 'stream=width,height',
               '-of', 'csv=s=x:p=0',
               filename]
    cmd_out, cmd_error = subprocess.Popen(
        command, stdout=subprocess.PIPE).communicate()
    cmd_out = cmd_out.decode()
    cover_width, cover_height = cmd_out.split("x")

    # extract frames
    out, _ = ffmpeg.input(filename).output(
        'pipe:', format='rawvideo', pix_fmt='rgb24').run(capture_stdout=True)

    frames = np.frombuffer(out, np.uint8).reshape(
        [-1, int(cover_height), int(cover_width), 3])
    
    return frames


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
