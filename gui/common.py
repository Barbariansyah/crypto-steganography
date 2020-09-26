import typing
from PyQt5.QtWidgets import *

APP_MODE: typing.List[str] = ['Image encode', 'Video encode', 'Audio encode', 'Image extract', 'Video extract', 'Audio extract']
FILE_TYPE_FILTER: typing.Dict[str, str] = {
    'Image': 'PNG Images (*.png);;BMP Images (*.bmp);;All Files (*)',
    'Video': 'AVI Videos (*.avi);;All Files (*)',
    'Audio': 'WAV Audios (*.wav);;All Files (*)',
    'Any': 'All Files (*)',
}
WIDGET_MIN_DIM = 360
IMAGE_MIN_DIM = 200
IMAGE_DIM = 480


def open_file(parent: QWidget, dialog_title: str, file_filter: str):
    file_name, _ = QFileDialog.getOpenFileName(parent, dialog_title, '', file_filter)
    
    if file_name:
        return file_name

def save_file(parent: QWidget, dialog_title: str, default_file_name: str, file_filter: str):
    file_name, _ = QFileDialog.getSaveFileName(parent, dialog_title, default_file_name, file_filter)
    
    if file_name:
        return file_name