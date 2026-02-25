import random
from PySide6.QtWidgets import QSplashScreen, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPixmap, QColor, QPainter
from PySide6.QtSvgWidgets import QSvgWidget

from core.config import ConfigManager
from core.utils import resource_path

def get_theme_colors():
    theme_name = ConfigManager().get("theme", "matcha")
    try:
        theme_module = __import__(f"gui.themes.{theme_name}", fromlist=['COLORS'])
        return theme_module.COLORS
    except ImportError:
        from gui.themes.matcha import COLORS
        return COLORS

class AudioScannerBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setFixedWidth(280)
        self.bars_count = 35
        self.bar_values = [5.0] * self.bars_count
        self.target_values = [5.0] * self.bars_count
        self.scan_pos = -20.0

        colors = get_theme_colors()
        self.accent_color = QColor(colors["ACCENT"])
        self.bg_color = QColor(colors["BORDER_DIM"])

        self.acc_rgb = (self.accent_color.red(), self.accent_color.green(), self.accent_color.blue())
        self.bg_rgb = (self.bg_color.red(), self.bg_color.green(), self.bg_color.blue())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_anim)
        self.timer.start(16)

    def update_anim(self):
        self.scan_pos += 3.0
        if self.scan_pos > self.width() + 50:
            self.scan_pos = -50
        for i in range(self.bars_count):
            if random.random() < 0.15:
                self.target_values[i] = random.uniform(4.0, self.height() - 2)
            diff = self.target_values[i] - self.bar_values[i]
            self.bar_values[i] += diff * 0.2
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        bar_w = self.width() / self.bars_count
        margin = 2.0

        for i in range(self.bars_count):
            x = i * bar_w
            h = self.bar_values[i]
            y = self.height() - h
            rect = QRectF(x + margin / 2, y, bar_w - margin, h)
            dist_to_scan = self.scan_pos - x

            if 0 < dist_to_scan < 60:
                intensity = 1.0 - (dist_to_scan / 60.0)

                r = int(self.bg_rgb[0] + (self.acc_rgb[0] - self.bg_rgb[0]) * intensity)
                g = int(self.bg_rgb[1] + (self.acc_rgb[1] - self.bg_rgb[1]) * intensity)
                b = int(self.bg_rgb[2] + (self.acc_rgb[2] - self.bg_rgb[2]) * intensity)

                painter.setBrush(QColor(r, g, b, 255))
            else:
                painter.setBrush(QColor(self.bg_rgb[0], self.bg_rgb[1], self.bg_rgb[2], 120))

            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, 2, 2)

        if 0 <= self.scan_pos <= self.width():
            painter.setBrush(QColor(255, 255, 255, 200))
            painter.drawRect(QRectF(self.scan_pos, 0, 2, self.height()))

class ModernSplashScreen(QSplashScreen):
    def __init__(self):
        transparent_pixmap = QPixmap(400, 450)
        transparent_pixmap.fill(QColor(0, 0, 0, 0))
        super().__init__(transparent_pixmap)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 400, 450)
        self.container.setObjectName("SplashContainer")

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(20, 20, 20, 20)

        logo_path = resource_path("assets/icon_nt_static.svg")
        self.logo = QSvgWidget(logo_path)
        self.logo.setFixedSize(360, 408)

        self.scanner_bar = AudioScannerBar()

        self.status_label = QLabel("Initializing VSTea Core...")
        self.status_label.setObjectName("SplashStatus")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(self.scanner_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(5)
        layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

    def show_message(self, msg):
        self.status_label.setText(msg)