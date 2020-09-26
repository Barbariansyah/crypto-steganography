from typing import Tuple
from steganography.util import string_to_binary, binary_to_int, binary_to_string

def audio_metadata_to_binary(encrypt: bool, sequential: bool, file_size: int, file_name: str) -> str:
    metadata_binary = ''
    metadata_binary += '0' if encrypt == False else '1'
    metadata_binary += '0' if sequential == False else '1'
    
    metadata_binary += format(file_size, '032b')
    file_name_binary = string_to_binary(file_name)
    metadata_binary += file_name_binary
    
    metadata_length = len(metadata_binary) + 16
    metadata_binary = format(metadata_length, '016b') + metadata_binary 
    
    return metadata_binary

def binary_to_audio_metadata(lsb_string: str) -> Tuple[bool, bool, int, str]:
    size = binary_to_int(lsb_string[:16])
    
    metadata_binary = lsb_string[16:size]
    encrypt = True if metadata_binary[0] == '1' else False
    sequential = True if metadata_binary[1] == '1' else False

    file_size = binary_to_int(metadata_binary[2:34])
    file_name = binary_to_string(metadata_binary[34:])

    return size, encrypt, sequential, file_size, file_name