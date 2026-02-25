from core.constants import APP_NAME, APP_VERSION, APP_AUTHOR
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

class AboutView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 50, 60, 50)
        layout.setSpacing(20)

        h1 = QLabel(f"About {APP_NAME}", objectName="H1")

        sub = QLabel(
            f"{APP_NAME} is a smart, cross-platform utility that scans your installed DAWs "
            "to create a comprehensive, unified library of your audio plugins.",
            objectName="Sub"
        )
        sub.setWordWrap(True)

        card = QFrame()
        card.setObjectName("AboutCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(12)

        def add_info_row(key_text, val_text):
            row = QHBoxLayout()
            lbl_key = QLabel(key_text, objectName="AboutKey")
            lbl_val = QLabel(val_text, objectName="AboutVal")
            row.addWidget(lbl_key)
            row.addWidget(lbl_val)
            row.addStretch()
            card_layout.addLayout(row)

        add_info_row("Version:", APP_VERSION)
        add_info_row("Built with:", "Python & PySide6")
        add_info_row("License:", "GPL-3.0")
        add_info_row("Developer:", APP_AUTHOR)

        btn_layout = QHBoxLayout()
        self.btn_github = QPushButton("⭐ View on GitHub")
        self.btn_github.setObjectName("PrimaryBtn")
        self.btn_github.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_github.clicked.connect(self.open_github)

        btn_layout.addWidget(self.btn_github)
        btn_layout.addStretch()

        layout.addWidget(h1)
        layout.addWidget(sub)
        layout.addSpacing(10)
        layout.addWidget(card)
        layout.addSpacing(20)
        layout.addLayout(btn_layout)
        layout.addStretch()

    def open_github(self):
        github_url = "https://github.com/Karaatin/VSTea"
        QDesktopServices.openUrl(QUrl(github_url))