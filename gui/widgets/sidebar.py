from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QWidget
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtSvgWidgets import QSvgWidget

from core.utils import resource_path

class Sidebar(QFrame):
    nav_clicked = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.sidebar_width = 220
        self.setMaximumWidth(self.sidebar_width)
        self.setMinimumWidth(0)

        self.anim = QPropertyAnimation(self, b"maximumWidth")
        self.anim.setDuration(400)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.nav_btns = []
        self._init_ui()

    def _init_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        self.content = QWidget()
        self.content.setFixedWidth(self.sidebar_width)

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(15, 30, 15, 30)
        layout.setSpacing(10)

        logo_path = resource_path("assets/icon_nt_static.svg")
        self.logo = QSvgWidget(logo_path)
        self.logo.setFixedSize(120, 136)
        layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(20)

        nav_items = [
            ("🎛️  Dashboard", 0),
            ("⚙️  Settings", 2),
            ("ℹ️  About", 3)
        ]

        for text, idx in nav_items:
            btn = QPushButton(text)
            btn.setObjectName("NavBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked=False, i=idx: self._on_button_clicked(i))
            layout.addWidget(btn)
            self.nav_btns.append((idx, btn))

        layout.addStretch()
        outer_layout.addWidget(self.content)
        self.set_active(0)

    def _on_button_clicked(self, index: int):
        self.set_active(index)
        self.nav_clicked.emit(index)

    def set_active(self, index: int):
        highlight_index = 0 if index == 1 else index
        for idx, btn in self.nav_btns:
            btn.setChecked(idx == highlight_index)

    def toggle(self):
        width = self.width()
        if width == 0:
            self.anim.setStartValue(0)
            self.anim.setEndValue(self.sidebar_width)
        else:
            self.anim.setStartValue(self.sidebar_width)
            self.anim.setEndValue(0)
        self.anim.start()