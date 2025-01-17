from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from os import path
from gui.common import FILE_TYPE_FILTER, IMAGE_DIM, open_file, save_file
from steganography import embed_to_video, extract_from_video, save_video, play_video, save_bytes_to_file


class VideoEncodeWidget(QWidget):
    def __init__(self, parent: QWidget):
        super(VideoEncodeWidget, self).__init__(parent)

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
        h_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.button_load_cover = QPushButton('Choose cover video', self)
        self.button_load_cover.clicked.connect(self._open_cover_video)
        h_frame_layout.addWidget(self.button_load_cover)

        self.button_save_stego = QPushButton('Save stego video', self)
        self.button_save_stego.clicked.connect(self._save_stego_video)
        self.button_save_stego.setDisabled(True)
        h_frame_layout.addWidget(self.button_save_stego)

        self.button_play_video = QPushButton('Play video', self)
        self.button_play_video.clicked.connect(self._play_video)
        h_frame_layout.addWidget(self.button_play_video)

        h_frame_widget.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_frame_widget.setLayout(h_frame_layout)
        self.layout.addWidget(h_frame_widget)

        # Add load embedded file
        self.button_load_embedded = QPushButton(
            'Choose file to be embedded', self)
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
        self.layout.addWidget(self._init_frame_seq_radio())
        self.layout.addWidget(self._init_pixel_seq_radio())

        # Add key input
        self.textbox_key = QLineEdit(self)
        self.textbox_key.setPlaceholderText('Stegano Key')
        self.layout.addWidget(self.textbox_key)

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

        button = QRadioButton('Without Encryption')
        encrypt_group.addButton(button)
        encrypt_radio_layout.addWidget(button)

        encrypt_radio_pane.setLayout(encrypt_radio_layout)
        return encrypt_radio_pane

    def _init_frame_seq_radio(self):
        frame_seq_radio_pane = QWidget()
        frame_seq_radio_layout = QHBoxLayout()
        frame_seq_radio_layout.setContentsMargins(0, 0, 0, 0)

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
        pixel_seq_radio_layout.setContentsMargins(0, 0, 0, 0)

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

    def _open_cover_video(self):
        self.cover_full_path = open_file(self, 'Choose cover video',
                                         FILE_TYPE_FILTER['Video'])
        if self.cover_full_path is None:
            return

        _, file_name = path.split(self.cover_full_path)
        self.original_file_name = file_name
        self.button_load_cover.setText(f'Chosen video: {file_name}')

    def _open_embedded_file(self):
        self.embed_full_path = open_file(
            self, 'Choose file to be embedded', FILE_TYPE_FILTER['Any'])
        if self.embed_full_path is None:
            return

        _, file_name = path.split(self.embed_full_path)
        self.button_load_embedded.setText(f'Chosen file: {file_name}')

    def _save_stego_video(self):
        stego_full_path = save_file(self, 'Chose save location',
                                    self.original_file_name, FILE_TYPE_FILTER['Video'])
        if stego_full_path is None:
            return

        save_video(self.stego_video, self.stego_video_params, stego_full_path, self.video_has_audio)

    def _play_video(self):
        self.video_full_path = open_file(
            self, 'Choose file to be played', FILE_TYPE_FILTER['Video'])
        if self.video_full_path is None:
            return

        play_video(self.video_full_path)

    def _steganify(self):
        try:
            self.stego_video, self.stego_video_params, psnr_value, self.video_has_audio = embed_to_video(
                self.embed_full_path,
                self.cover_full_path,
                self.textbox_key.text(),
                self.encrypt,
                self.pixel_seq,
                self.frame_seq
            )
            self.button_play_video.setDisabled(False)
            self.button_save_stego.setDisabled(False)

            message = QMessageBox(
                QMessageBox.NoIcon,
                'Steganify',
                f'File succesfully embedded with PSNR {psnr_value:0.2f} dB'
            )
            message.exec()
        except Exception as e:
            print(e)
            message = QMessageBox(
                QMessageBox.Critical,
                'Steganify',
                'Embedded file size is too big for cover capacity'
            )
            message.exec()

    def _encrypt_choice_cb(self, state: QRadioButton):
        self.encrypt = True if state.text() == 'With encryption' else False

    def _frame_seq_choice_cb(self, state: QRadioButton):
        self.frame_seq = True if state.text() == 'Frame sequential' else False

    def _pixel_seq_choice_cb(self, state: QRadioButton):
        self.pixel_seq = True if state.text() == 'Pixel sequential' else False


class VideoDecodeWidget(QWidget):
    def __init__(self, parent: QWidget):
        super(VideoDecodeWidget, self).__init__(parent)

        self._init_ui()

    def _init_ui(self):
        # Init layout
        self.layout = QVBoxLayout(self)

        # Add load stego video and save extracted file
        h_frame_widget = QWidget()
        h_frame_layout = QHBoxLayout()
        h_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.button_load_stego = QPushButton('Load stego video', self)
        self.button_load_stego.clicked.connect(self._load_stego_video)
        h_frame_layout.addWidget(self.button_load_stego)

        self.button_play_video = QPushButton('Play video', self)
        self.button_play_video.clicked.connect(self._play_video)
        h_frame_layout.addWidget(self.button_play_video)

        self.button_save_extracted = QPushButton('Save extracted file', self)
        self.button_save_extracted.clicked.connect(self._save_extracted_file)
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

    def _load_stego_video(self):
        self.stego_full_path = open_file(self, 'Choose stego video',
                                         FILE_TYPE_FILTER['Video'])
        if self.stego_full_path is None:
            return

        _, file_name = path.split(self.stego_full_path)
        self.button_load_stego.setText(f'Chosen video: {file_name}')

    def _play_video(self):
        self.video_full_path = open_file(
            self, 'Choose file to be played', FILE_TYPE_FILTER['Video'])
        if self.video_full_path is None:
            return

        play_video(self.video_full_path)

    def _save_extracted_file(self):
        full_path = save_file(self, 'Save extracted file',
                              self.embed_file_name, FILE_TYPE_FILTER['Any'])
        if full_path is None:
            return

        save_bytes_to_file(self.embed_bytes, full_path)

    def _desteganify(self):
        try:
            self.embed_bytes, self.embed_file_name = extract_from_video(
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
        except Exception as e:
            message = QMessageBox(
                QMessageBox.Critical,
                'Desteganify',
                'Failed to extract embedded file'
            )
            message.exec()
