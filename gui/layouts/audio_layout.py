from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import path
from gui.common import FILE_TYPE_FILTER, IMAGE_DIM, open_file, save_file
from steganography.image_steganography import lsb

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

        self.button_load_container = QPushButton('Choose container audio', self)
        self.button_load_container.clicked.connect(self._open_container_audio)
        h_frame_layout.addWidget(self.button_load_container)

        self.button_save_payloaded = QPushButton('Save payloaded audio', self)
        self.button_save_payloaded.clicked.connect(self._save_payloaded_audio)
        self.button_save_payloaded.setDisabled(True)
        h_frame_layout.addWidget(self.button_save_payloaded)

        h_frame_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_frame_widget.setLayout(h_frame_layout)
        self.layout.addWidget(h_frame_widget)

        # Add load to be hidden file
        self.button_load_hidden = QPushButton('Choose file to be hidden', self)
        self.button_load_hidden.clicked.connect(self._open_hidden_file)
        self.layout.addWidget(self.button_load_hidden)

        # Add stegano properties config
        self._init_stegano_properties_ui()

        # Add steganify button
        self.button_steganify = QPushButton('Steganify!', self)
        self.button_steganify.clicked.connect(self._steganify)
        self.layout.addWidget(self.button_steganify)

        # Add psnr info label
        self.label_psnr = QLabel('File succesfully hidden with PSNR: ', self)
        self.label_psnr.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.label_psnr.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_psnr)

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

    def _open_container_audio(self):
        full_path = open_file('Choose container audio', FILE_TYPE_FILTER['Audio'])
        if full_path is None:
            return

        _, file_name = path.split(full_path)
        self.original_image = QPixmap(full_path)

        self.button_load_container.setText(f'Chosen audio: {file_name}')
        self.image_l.setPixmap(self.original_image)
    
    def _open_hidden_file(self):
        full_path = open_file('Choose file to be hidden', FILE_TYPE_FILTER['Any'])
        if full_path is None:
            return

        _, file_name = path.split(full_path)
        self.button_load_container.setText(f'Chosen file: {file_name}')

    def _save_payloaded_audio(self):
        full_path = save_file('Chose save location', FILE_TYPE_FILTER['Audio'])
        print(full_path)

    def _steganify(self):
        # payloaded_file, psnr = lsb.embed_to_image(...)
        # self.payloaded_image = QPixmap.loadFromData(payloaded_file)
        # self.button_save_payloaded.setDisabled(False)
        # self.label_psnr.setText(psnr)
        pass
    
    def _encrypt_choice_cb(self, state: QRadioButton):
        self.encrypt = True if state.text() == 'With encryption' else False
    
    def _sequential_choice_cb(self, state: QRadioButton):
        self.sequential = True if state.text() == 'Sequential' else False