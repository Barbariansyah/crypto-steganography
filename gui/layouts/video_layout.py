from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import path
from gui.common import FILE_TYPE_FILTER, IMAGE_DIM
from steganography.image_steganography import lsb

class VideoEncodeWidget(QWidget):
    def __init__(self, parent: QWidget):
        super(VideoEncodeWidget, self).__init__(parent)
        self.original_image = None
        self.payloaded_image = None

        # Stegano properties
        self.encrypt = True
        self.frame_seq = True
        self.pixel_seq = True

        self._init_ui()

    def _init_ui(self):
        # Init layout
        self.layout = QVBoxLayout(self)

        # Add load and save video
        h_frame_widget = QWidget()
        h_frame_layout = QHBoxLayout()
        h_frame_layout.setContentsMargins(0,0,0,0)

        self.button_load_container = QPushButton('Choose container video', self)
        self.button_load_container.clicked.connect(self._open_container_video)
        h_frame_layout.addWidget(self.button_load_container)

        self.button_save_payloaded = QPushButton('Save payloaded video', self)
        self.button_save_payloaded.clicked.connect(self._save_payloaded_video)
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
        self.layout.addWidget(self._init_frame_seq_radio())
        self.layout.addWidget(self._init_pixel_seq_radio())

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

    def _init_frame_seq_radio(self):
        frame_seq_radio_pane = QWidget()
        frame_seq_radio_layout = QHBoxLayout()
        frame_seq_radio_layout.setContentsMargins(0,0,0,0)

        frame_seq_group = QButtonGroup(self)
        frame_seq_group.buttonClicked.connect(self._frame_seq_choice_cb)

        button = QRadioButton('Frame sequential')
        button.setChecked(True)
        frame_seq_group.addButton(button)
        frame_seq_radio_layout.addWidget(button)

        button = QRadioButton('Frame random')
        frame_seq_group.addButton(button)
        frame_seq_radio_layout.addWidget(button)

        frame_seq_radio_pane.setLayout(frame_seq_radio_layout)
        return frame_seq_radio_pane

    def _init_pixel_seq_radio(self):
        pixel_seq_radio_pane = QWidget()
        pixel_seq_radio_layout = QHBoxLayout()
        pixel_seq_radio_layout.setContentsMargins(0,0,0,0)

        pixel_seq_group = QButtonGroup(self)
        pixel_seq_group.buttonClicked.connect(self._pixel_seq_choice_cb)

        button = QRadioButton('Pixel sequential')
        button.setChecked(True)
        pixel_seq_group.addButton(button)
        pixel_seq_radio_layout.addWidget(button)

        button = QRadioButton('Pixel random')
        pixel_seq_group.addButton(button)
        pixel_seq_radio_layout.addWidget(button)

        pixel_seq_radio_pane.setLayout(pixel_seq_radio_layout)
        return pixel_seq_radio_pane

    def _open_file(self, dialog_title: str, file_filter: str):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, dialog_title, '', file_filter, options=options)
        
        if file_name:
            return file_name

    def _open_container_video(self):
        full_path = self._open_file('Choose container video', FILE_TYPE_FILTER['Video'])
        if full_path is None:
            return

        _, file_name = path.split(full_path)
        self.original_image = QPixmap(full_path)

        self.button_load_container.setText(f'Chosen video: {file_name}')
        self.image_l.setPixmap(self.original_image)
    
    def _open_hidden_file(self):
        full_path = self._open_file('Choose file to be hidden', FILE_TYPE_FILTER['Any'])
        if full_path is None:
            return

        _, file_name = path.split(full_path)
        self.button_load_container.setText(f'Chosen file: {file_name}')

    def _save_payloaded_video(self):
        pass

    def _steganify(self):
        # payloaded_file, psnr = lsb.embed_to_image(...)
        # self.payloaded_image = QPixmap.loadFromData(payloaded_file)
        # self.button_save_payloaded.setDisabled(False)
        # self.label_psnr.setText(psnr)
        pass
    
    def _encrypt_choice_cb(self, state: QRadioButton):
        self.encrypt = True if state.text() == 'With encryption' else False
    
    def _frame_seq_choice_cb(self, state: QRadioButton):
        self.frame_seq = True if state.text() == 'Frame sequential' else False
    
    def _pixel_seq_choice_cb(self, state: QRadioButton):
        self.pixel_seq = True if state.text() == 'Pixel sequential' else False