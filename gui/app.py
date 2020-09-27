import typing
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui.layouts.image_layout import ImageEncodeWidget, ImageDecodeWidget
from gui.layouts.video_layout import VideoEncodeWidget, VideoDecodeWidget
from gui.layouts.audio_layout import AudioEncodeWidget, AudioDecodeWidget
from gui.common import APP_MODE, WIDGET_MIN_DIM


class MainWidget(QWidget):
    def __init__(self, parent: QWidget):
        super(MainWidget, self).__init__(parent)
        self.mode_widget: typing.Dict[QWidget] = dict()
        self._init_ui()

    def _init_ui(self):
        # Init layout
        layout = QVBoxLayout(self)

        # Init default (none) widget
        self.mode_widget['None'] = QLabel('Choose a mode', self)
        self.mode_widget['None'].setMinimumSize(WIDGET_MIN_DIM, WIDGET_MIN_DIM)
        self.mode_widget['None'].setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mode_widget['None'].setAlignment(Qt.AlignCenter)
        layout.addWidget(self.mode_widget['None'])

        # Init all mode widget
        self.mode_widget['Image encode'] = ImageEncodeWidget(self)
        self.mode_widget['Image encode'].setHidden(True)
        layout.addWidget(self.mode_widget['Image encode'])

        self.mode_widget['Image extract'] = ImageDecodeWidget(self)
        self.mode_widget['Image extract'].setHidden(True)
        layout.addWidget(self.mode_widget['Image extract'])

        self.mode_widget['Video encode'] = VideoEncodeWidget(self)
        self.mode_widget['Video encode'].setHidden(True)
        layout.addWidget(self.mode_widget['Video encode'])

        self.mode_widget['Video extract'] = VideoDecodeWidget(self)
        self.mode_widget['Video extract'].setHidden(True)
        layout.addWidget(self.mode_widget['Video extract'])

        self.mode_widget['Audio encode'] = AudioEncodeWidget(self)
        self.mode_widget['Audio encode'].setHidden(True)
        layout.addWidget(self.mode_widget['Audio encode'])

        self.mode_widget['Audio extract'] = AudioDecodeWidget(self)
        self.mode_widget['Audio extract'].setHidden(True)
        layout.addWidget(self.mode_widget['Audio extract'])

        self.setLayout(layout)

    def redraw_ui(self, active_mode: str):
        modes = APP_MODE + ['None']
        for mode in modes:
            if mode == active_mode:
                self.mode_widget[mode].setHidden(False)
            else:
                self.mode_widget[mode].setHidden(True)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Steganify'
        self.left = 150
        self.top = 150
        self.width = 640
        self.height = 480
        self.mode = 'None'
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Add menu
        self._init_menu()

        # Init main widget
        self.main_widget = MainWidget(self)

        self.setCentralWidget(self.main_widget)
        self.show()

    def _init_menu(self):
        menu = self.menuBar()

        mode_menu = menu.addMenu('Mode')
        mode_menu.triggered.connect(self._menu_cb)

        # Add modes
        self.mode_actions = []
        modes = APP_MODE
        for mode in modes:
            imageMode = QAction(mode, self)
            imageMode.setCheckable(True)
            self.mode_actions.append(imageMode)
            mode_menu.addAction(imageMode)

    def _menu_cb(self, action: QAction):
        new_mode = action.text() if action.isChecked() else 'None'
        self.mode = new_mode
        self.main_widget.redraw_ui(self.mode)
        self._set_actions(self.mode)
        self.resize(self.minimumSizeHint())

    def _set_actions(self, mode: str):
        for action in self.mode_actions:
            if action.text() != mode:
                action.setChecked(False)
