from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui.image_layout import ImageEncodeWidget

class MainWidget(QWidget):
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self._init_ui()

    def _init_ui(self):
        # Init layout
        layout = QVBoxLayout(self)

        # Init active widget
        self.text_info = QLabel('Choose a mode', self)
        self.text_info.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.text_info)

        # Init and hide specific operation widget
        self.image_widget = ImageEncodeWidget(self)
        self.image_widget.setHidden(True)
        layout.addWidget(self.image_widget)

        self.setLayout(layout)

    def redraw_ui(self, mode):
        if mode == 'None':
            self.text_info.setText('Choose a mode')

        if mode == 'Image':
            self.image_widget.setHidden(False)
            self.text_info.setHidden(True)
        else:
            self.image_widget.setHidden(True)
            self.text_info.setHidden(False)

        if mode == 'Video':
            self.text_info.setText('Video mode')

        if mode == 'Audio':
            self.text_info.setText('Audio mode')


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Stegano Tools'
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
        modes = ['Image', 'Video', 'Audio']
        for mode in modes:
            imageMode = QAction(mode, self)
            imageMode.setCheckable(True)
            self.mode_actions.append(imageMode)
            mode_menu.addAction(imageMode)
        
    def _menu_cb(self, action):
        new_mode = action.text() if action.isChecked() else 'None'
        self._set_mode(new_mode)

    def _set_mode(self, mode):
        self.mode = mode

        for action in self.mode_actions:
            if action.text() != mode:
                action.setChecked(False)

        self.main_widget.redraw_ui(self.mode)
