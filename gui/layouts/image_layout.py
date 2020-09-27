from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import path
from gui.common import FILE_TYPE_FILTER, IMAGE_DIM, IMAGE_MIN_DIM, open_file, save_file
from steganography import embed_to_image, extract_from_image


class ImageEncodeWidget(QWidget):
    def __init__(self, parent: QWidget):
        super(ImageEncodeWidget, self).__init__(parent)
        self.cover_image = None
        self.stego_image = None

        # Stegano properties
        self.encrypt = True
        self.method = 'lsb'
        self.sequential = True

        self._init_ui()

    def _init_ui(self):
        # Init layout
        self.layout = QVBoxLayout(self)

        # Add image frames
        h_frame_widget = QWidget()
        h_frame_layout = QHBoxLayout()

        h_frame_layout.addWidget(self._init_cover_image_ui())
        h_frame_layout.addWidget(self._init_stego_image_ui())
        h_frame_layout.setContentsMargins(0, 0, 0, 0)

        h_frame_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        h_frame_widget.setLayout(h_frame_layout)
        self.layout.addWidget(h_frame_widget)

        # Add load embedded file
        self.button_load_embed = QPushButton(
            'Choose file to be embedded', self)
        self.button_load_embed.clicked.connect(self._open_embedded_file)
        self.layout.addWidget(self.button_load_embed)

        # Add stegano properties config
        self._init_stegano_properties_ui()

        # Add steganify button
        self.button_steganify = QPushButton('Steganify!', self)
        self.button_steganify.clicked.connect(self._steganify)
        self.layout.addWidget(self.button_steganify)

        self.setLayout(self.layout)

    def _init_cover_image_ui(self):
        cover_image_pane = QWidget()
        cover_image_layout = QVBoxLayout()
        cover_image_layout.setContentsMargins(0, 0, 0, 0)

        self.image_l = QLabel(cover_image_pane)
        self.image_l.setFrameStyle(QFrame.Box)
        self.image_l.setMinimumSize(IMAGE_MIN_DIM, IMAGE_MIN_DIM)
        self.image_l.setMaximumSize(IMAGE_DIM, IMAGE_DIM)
        self.image_l.setScaledContents(True)
        cover_image_layout.addWidget(self.image_l)

        self.button_load_cover = QPushButton('Choose cover image', self)
        self.button_load_cover.clicked.connect(self._open_cover_image)
        cover_image_layout.addWidget(self.button_load_cover)

        cover_image_pane.setLayout(cover_image_layout)
        return cover_image_pane

    def _init_stego_image_ui(self):
        stego_image_pane = QWidget()
        stego_image_layout = QVBoxLayout()
        stego_image_layout.setContentsMargins(0, 0, 0, 0)

        self.image_r = QLabel(stego_image_pane)
        self.image_r.setFrameStyle(QFrame.Box)
        self.image_r.setMinimumSize(IMAGE_MIN_DIM, IMAGE_MIN_DIM)
        self.image_r.setMaximumSize(IMAGE_DIM, IMAGE_DIM)
        self.image_r.setScaledContents(True)
        stego_image_layout.addWidget(self.image_r)

        self.button_save_stego = QPushButton('Save stego image', self)
        self.button_save_stego.clicked.connect(self._save_stego_image)
        self.button_save_stego.setDisabled(True)
        stego_image_layout.addWidget(self.button_save_stego)

        stego_image_pane.setLayout(stego_image_layout)
        return stego_image_pane

    def _init_stegano_properties_ui(self):
        self.layout.addWidget(self._init_encrypt_radio())
        self.layout.addWidget(self._init_method_radio())
        self.layout.addWidget(self._init_sequential_radio())

        # Add key input
        self.textbox_key = QLineEdit(self)
        self.textbox_key.setPlaceholderText('Stegano Key')
        self.layout.addWidget(self.textbox_key)

        # Add threshold input
        self.textbox_threshold = QLineEdit(self)
        self.textbox_threshold.setPlaceholderText('BPCS Threshold')
        self.textbox_threshold.setText('0.3')
        self.layout.addWidget(self.textbox_threshold)

    def _init_encrypt_radio(self):
        encrypt_radio_pane = QWidget()
        encrypt_radio_layout = QHBoxLayout()
        encrypt_radio_layout.setContentsMargins(0, 0, 0, 0)

        encrypt_group = QButtonGroup(self)
        encrypt_group.buttonClicked.connect(self._encrypt_choice_cb)

        button = QRadioButton('With encryption')
        button.setChecked(True)
        encrypt_group.addButton(button)
        encrypt_radio_layout.addWidget(button)

        button = QRadioButton('Without encryption')
        encrypt_group.addButton(button)
        encrypt_radio_layout.addWidget(button)

        encrypt_radio_pane.setLayout(encrypt_radio_layout)
        return encrypt_radio_pane

    def _init_method_radio(self):
        method_radio_pane = QWidget()
        method_radio_layout = QHBoxLayout()
        method_radio_layout.setContentsMargins(0, 0, 0, 0)

        method_group = QButtonGroup(self)
        method_group.buttonClicked.connect(self._method_choice_cb)

        button = QRadioButton('LSB')
        button.setChecked(True)
        method_group.addButton(button)
        method_radio_layout.addWidget(button)

        button = QRadioButton('BPCS')
        method_group.addButton(button)
        method_radio_layout.addWidget(button)

        method_radio_pane.setLayout(method_radio_layout)
        return method_radio_pane

    def _init_sequential_radio(self):
        sequential_radio_pane = QWidget()
        sequential_radio_layout = QHBoxLayout()
        sequential_radio_layout.setContentsMargins(0, 0, 0, 0)

        sequential_group = QButtonGroup(self)
        sequential_group.buttonClicked.connect(self._sequential_choice_cb)

        button = QRadioButton('Sequential')
        button.setChecked(True)
        sequential_group.addButton(button)
        sequential_radio_layout.addWidget(button)

        button = QRadioButton('Random')
        sequential_group.addButton(button)
        sequential_radio_layout.addWidget(button)

        sequential_radio_pane.setLayout(sequential_radio_layout)
        return sequential_radio_pane

    def _open_cover_image(self):
        self.cover_full_path = open_file(
            self, 'Choose cover image', FILE_TYPE_FILTER['Image'])
        if self.cover_full_path is None:
            return

        _, file_name = path.split(self.cover_full_path)
        self.cover_image = QPixmap(self.cover_full_path)

        self.button_load_cover.setText(f'Chosen image: {file_name}')
        self.image_l.setPixmap(self.cover_image)

    def _open_embedded_file(self):
        self.embed_full_path = open_file(
            self, 'Choose file to be embedded', FILE_TYPE_FILTER['Any'])
        if self.embed_full_path is None:
            return

        _, file_name = path.split(self.embed_full_path)
        self.button_load_embed.setText(f'Chosen file: {file_name}')

    def _save_stego_image(self):
        # TODO: Save file outside embed function
        full_path = save_file(self, 'Chose save location',
                              '', FILE_TYPE_FILTER['Image'])
        print(full_path)

    def _steganify(self):
        # TODO: Return image and psnr value
        embed_to_image(
            self.embed_full_path,
            self.cover_full_path,
            self.textbox_key.text(),
            self.method,
            self.encrypt,
            self.sequential,
            float(self.textbox_threshold.text())
        )

        message = QMessageBox(
            QMessageBox.NoIcon,
            'Steganify',
            f'File succesfully embedded with PSNR ???'
        )
        message.exec()

    def _encrypt_choice_cb(self, state: QRadioButton):
        self.encrypt = True if state.text() == 'With encryption' else False

    def _method_choice_cb(self, state: QRadioButton):
        self.method = 'lsb' if state.text() == 'LSB' else 'bpcs'

    def _sequential_choice_cb(self, state: QRadioButton):
        self.sequential = True if state.text() == 'Sequential' else False


class ImageDecodeWidget(QWidget):
    def __init__(self, parent: QWidget):
        super(ImageDecodeWidget, self).__init__(parent)

        self._init_ui()

    def _init_ui(self):
        # Init layout
        self.layout = QVBoxLayout(self)

        # Add load stego image and save extracted file
        h_frame_widget = QWidget()
        h_frame_layout = QHBoxLayout()
        h_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.button_load_stego = QPushButton('Load stego image', self)
        self.button_load_stego.clicked.connect(self._load_stego_image)
        h_frame_layout.addWidget(self.button_load_stego)

        self.button_save_extracted = QPushButton('Save extracted file', self)
        self.button_save_extracted.clicked.connect(self._save_extracted_image)
        self.button_save_extracted.setDisabled(True)
        h_frame_layout.addWidget(self.button_save_extracted)

        h_frame_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_frame_widget.setLayout(h_frame_layout)
        self.layout.addWidget(h_frame_widget)

        # Add key input
        self.textbox_key = QLineEdit(self)
        self.textbox_key.setPlaceholderText('Stegano Key')
        self.layout.addWidget(self.textbox_key)

        # Add extract button
        self.button_steganify = QPushButton('De-Steganify!', self)
        self.button_steganify.clicked.connect(self._desteganify)
        self.layout.addWidget(self.button_steganify)

        self.setLayout(self.layout)

    def _load_stego_image(self):
        self.stego_full_path = open_file(
            self, 'Choose stego image', FILE_TYPE_FILTER['Image'])
        if self.stego_full_path is None:
            return

        _, file_name = path.split(self.stego_full_path)
        self.button_load_stego.setText(f'Chosen image: {file_name}')

    def _save_extracted_image(self):
        # TODO: Save file outside embed function
        full_path = save_file(self, 'Save extracted file',
                              '', FILE_TYPE_FILTER['Any'])
        print(full_path)

    def _desteganify(self):
        # TODO: Return extracted file and psnr value
        extract_from_image(self.stego_full_path, self.textbox_key.text())
        message = QMessageBox(
            QMessageBox.NoIcon,
            'Desteganify',
            'Successfully extracted'
        )
        message.exec()
