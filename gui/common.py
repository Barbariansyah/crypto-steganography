import typing

APP_MODE: typing.List[str] = ['Image encode', 'Video encode', 'Audio encode', 'Image extract', 'Video extract', 'Audio extract']
FILE_TYPE_FILTER: typing.Dict[str, str] = {
    'Image': 'PNG Images (*.png);;BMP Images (*.bmp)',
    'Video': 'AVI Videos (*.avi)',
    'Audio': 'WAV Videos (*.wav)',
    'Any': 'All Files (*)',
}
IMAGE_DIM = 480
