import typing

APP_MODE: typing.List[str] = ['Image encode', 'Video encode', 'Audio encode', 'Image extract', 'Video extract', 'Audio extract']
FILE_TYPE_FILTER: typing.Dict[str, str] = {
    'Image': 'PNG Images (*.png);;BMP Images (*.bmp);;All Files (*)',
    'Video': 'AVI Videos (*.avi);;All Files (*)',
    'Audio': 'WAV Videos (*.wav);;All Files (*)',
    'Any': 'All Files (*)',
}
WIDGET_MIN_DIM = 360
IMAGE_MIN_DIM = 200
IMAGE_DIM = 480
