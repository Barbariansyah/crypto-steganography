from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import path
from gui.common import FILE_TYPE_FILTER, IMAGE_DIM, open_file, save_file
from steganography import embed_to_audio, extract_from_audio, save_audio, save_bytes_to_file

class AudioEncodeWidget(QWidget):
    def __init__(self, parent: QWidget):
        super(AudioEncodeWidget, self).__init__(parent)
        
        # Stegano properties
        self.encrypt = True
        self.sequential = True

        self._init_ui()

    def _init_ui(self):
        # Init layout
        self.layout = QVBoxLayout(self)

        # Add load and save audio
        h_frame_widget = QWidget()
        h_frame_layout = QHBoxLayout()
        h_frame_layout.setContentsMargins(0,0,0,0)

        self.button_load_cover = QPushButton('Choose cover audio', self)
        self.button_load_cover.clicked.connect(self._open_cover_audio)
        h_frame_layout.addWidget(self.button_load_cover)

        self.button_save_stego = QPushButton('Save stego audio', self)
        self.button_save_stego.clicked.connect(self._save_stego_audio)
        self.button_save_stego.setDisabled(True)
        h_frame_layout.addWidget(self.button_save_stego)

        h_frame_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_frame_widget.setLayout(h_frame_layout)
        self.layout.addWidget(h_frame_widget)

        # Add load to be embedded file
        self.button_load_embedded = QPushButton('Choose file to be embedded', self)
        self.button_load_embedded.clicked.connect(self._open_embedded_file)
        self.layout.addWidget(self.button_load_embedded)

        # Add stegano properties config
        self._init_stegano_properties_ui()

        # Add steganify button
        self.button_steganify = QPushButton('Steganify!', self)
        self.button_steganify.clicked.connect(self._steganify)
        self.layout.addWidget(self.button_steganify)

        self.setLayout(self.layout)

    def _init_stegano_properties_ui(self):
        self.layout.addWidget(self._init_encrypt_radio())
        self.layout.addWidget(self._init_sequential_radio())

        # Add key input
        self.textbox_key = QLineEdit(self)
        self.textbox_key.setPlaceholderText('Stegano Key')
        self.layout.addWidget(self.textbox_key)

    def _init_encrypt_radio(self):
        encrypt_radio_pane = QWidget()
        encrypt_radio_layout = QHBoxLayout()
        encrypt_radio_layout.setContentsMargins(0,0,0,0)

        encrypt_group = QButtonGroup(self)
        encrypt_group.buttonClicked.connect(self._encrypt_choice_cb)

        button = QRadioButton('With encryption')
        button.setChecked(True)
        encrypt_group.addButton(button)
        encrypt_radio_layout.addWidget(button)

        button = QRadioButton('Without Encryption')
        encrypt_group.addButton(button)
        encrypt_radio_layout.addWidget(button)

        encrypt_radio_pane.setLayout(encrypt_radio_layout)
        return encrypt_radio_pane

    def _init_sequential_radio(self):
        sequential_radio_pane = QWidget()
        sequential_radio_layout = QHBoxLayout()
        sequential_radio_layout.setContentsMargins(0,0,0,0)

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

    def _open_cover_audio(self):
        self.cover_full_path = open_file(self, 'Choose cover audio', FILE_TYPE_FILTER['Audio'])
        if self.cover_full_path is None:
            return

        _, file_name = path.split(self.cover_full_path)
        self.button_load_cover.setText(f'Chosen audio: {file_name}')
    
    def _open_embedded_file(self):
        self.embed_full_path = open_file(self, 'Choose file to be embedded', FILE_TYPE_FILTER['Any'])
        if self.embed_full_path is None:
            return

        _, file_name = path.split(self.embed_full_path)
        self.button_load_embedded.setText(f'Chosen file: {file_name}')

    def _save_stego_audio(self):
        stego_full_path = save_file(self, 'Chose save location', '', FILE_TYPE_FILTER['Audio'])
        save_audio(self.stego_audio, self.stego_audio_params, stego_full_path)

    def _steganify(self):
        self.stego_audio, self.stego_audio_params, psnr_value = embed_to_audio(
            self.embed_full_path, 
            self.cover_full_path, 
            self.textbox_key.text(), 
            self.encrypt, 
            self.sequential
        )
        self.button_save_stego.setDisabled(False)
        
        message = QMessageBox(
            QMessageBox.NoIcon, 
            'Steganify', 
            f'File succesfully embedded with PSNR {psnr_value}'
        )
        message.exec()
    
    def _encrypt_choice_cb(self, state: QRadioButton):
        self.encrypt = True if state.text() == 'With encryption' else False
    
    def _sequential_choice_cb(self, state: QRadioButton):
        self.sequential = True if state.text() == 'Sequential' else False

class AudioDecodeWidget(QWidget):
    def __init__(self, parent: QWidget):
        super(AudioDecodeWidget, self).__init__(parent)

        self._init_ui()

    def _init_ui(self):
        # Init layout
        self.layout = QVBoxLayout(self)

        # Add load stego audio and save extracted file
        h_frame_widget = QWidget()
        h_frame_layout = QHBoxLayout()
        h_frame_layout.setContentsMargins(0,0,0,0)

        self.button_load_stego = QPushButton('Load stego audio', self)
        self.button_load_stego.clicked.connect(self._load_stego_audio)
        h_frame_layout.addWidget(self.button_load_stego)

        self.button_save_extracted = QPushButton('Save extracted file', self)
        self.button_save_extracted.clicked.connect(self._save_extracted_file)
        self.button_save_extracted.setDisabled(True)
        h_frame_layout.addWidget(self.button_save_extracted)

        h_frame_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
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

    def _load_stego_audio(self):
        self.stego_full_path = open_file(self, 'Choose stego audio', FILE_TYPE_FILTER['Audio'])
        if self.stego_full_path is None:
            return

        _, file_name = path.split(self.stego_full_path)
        self.button_load_stego.setText(f'Chosen audio: {file_name}')
        self.button_save_extracted.setDisabled(True)

    def _save_extracted_file(self):
        full_path = save_file(self, 'Save extracted file', self.embed_file_name, FILE_TYPE_FILTER['Any'])
        save_bytes_to_file(self.embed_bytes, full_path)

    def _desteganify(self):
        self.embed_bytes, self.embed_file_name = extract_from_audio(
            self.stego_full_path,
            self.textbox_key.text()
        )
        self.button_save_extracted.setDisabled(False)
        
        message = QMessageBox(
            QMessageBox.NoIcon, 
            'Desteganify', 
            f'Successfully extracted {self.embed_file_name}'
        )
        message.exec()