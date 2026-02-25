from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QCheckBox, QPushButton, QFileDialog, QProgressBar)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter, QColor, QPen


class DawCardWidget(QWidget):
    path_changed = Signal(str, str)
    auto_detect_requested = Signal(str)

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.daw_id_str = session.id.value

        self.setMinimumWidth(250)
        self.setMaximumWidth(500)
        self.setFixedHeight(140)

        self.setAttribute(Qt.WidgetAttribute.WA_Hover)

        self.init_ui()
        self.update_state()

    def enterEvent(self, event):
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        from PySide6.QtGui import QPainter, QColor, QPen
        from PySide6.QtCore import Qt

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        theme_name = "matcha"
        main_win = self.window()
        if hasattr(main_win, "controller"):
            theme_name = main_win.controller.config.get("theme", "matcha")

        try:
            theme_module = __import__(f"gui.themes.{theme_name}", fromlist=['COLORS'])
            COLORS = theme_module.COLORS
        except ImportError:
            from gui.themes.matcha import COLORS

        status = self.property("cardStatus") or "missing"

        if status == "missing":
            bg_color = QColor(0, 0, 0, 0)
            border_color = QColor(COLORS["BORDER_DIM"])
            pen = QPen(border_color, 2, Qt.PenStyle.DashLine)

        elif status == "error":
            bg_color = QColor(COLORS["ERROR_BG"])
            border_color = QColor(COLORS["ERROR"])
            pen = QPen(border_color, 2, Qt.PenStyle.SolidLine)

        else:
            if self.underMouse():
                bg_color = QColor(COLORS["BG_HOVER"])
                border_color = QColor(COLORS.get("SUCCESS", COLORS["ACCENT_HL"]))
            else:
                bg_color = QColor(COLORS["BG_CARD"])
                border_color = QColor(COLORS.get("SUCCESS", COLORS["ACCENT"]))
            pen = QPen(border_color, 2, Qt.PenStyle.SolidLine)

        painter.setBrush(bg_color)
        painter.setPen(pen)

        rect = self.rect().adjusted(2, 2, -2, -2)
        painter.drawRoundedRect(rect, 12, 12)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(8)

        header = QHBoxLayout()
        self.lbl_name = QLabel(self.session.name)
        self.lbl_name.setObjectName("CardName")

        self.toggle = QCheckBox()
        self.toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle.stateChanged.connect(self.on_toggle)

        header.addWidget(self.lbl_name)
        header.addStretch()
        header.addWidget(self.toggle)
        layout.addLayout(header)

        self.lbl_info = QLabel()
        self.lbl_info.setWordWrap(True)
        self.lbl_info.setObjectName("CardInfo")
        self.lbl_info.setFixedHeight(30)
        self.lbl_info.setCursor(Qt.CursorShape.PointingHandCursor)

        self.loader = QProgressBar()
        self.loader.setFixedHeight(4)
        self.loader.setRange(0, 0)
        self.loader.setVisible(False)
        self.loader.setObjectName("CardLoader")

        layout.addWidget(self.lbl_info)
        layout.addWidget(self.loader)
        layout.addStretch()

        footer = QHBoxLayout()
        footer.setSpacing(8)

        # Der LED Status Punkt
        self.status_dot = QLabel()
        self.status_dot.setObjectName("StatusDot")
        self.status_dot.setFixedSize(10, 10)

        self.badge = QLabel()
        self.badge.setObjectName("Badge")

        self.btn_auto = QPushButton("✨")
        self.btn_auto.setObjectName("CardIconBtn")
        self.btn_auto.setToolTip("Auto-Detect default path")
        self.btn_auto.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_auto.clicked.connect(lambda: self.auto_detect_requested.emit(self.daw_id_str))

        self.btn_edit = QPushButton("📂")
        self.btn_edit.setObjectName("CardIconBtn")
        self.btn_edit.setToolTip("Manually set installation folder")
        self.btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit.clicked.connect(self.select_folder)

        footer.addWidget(self.status_dot)
        footer.addWidget(self.badge)
        footer.addStretch()
        footer.addWidget(self.btn_auto)
        footer.addWidget(self.btn_edit)

        layout.addLayout(footer)

    def _format_path(self, path_obj) -> str:
        parts = path_obj.parts
        if len(parts) > 3:
            return f"{parts[0]}.../{parts[-2]}/{parts[-1]}"
        return str(path_obj)

    def _apply_status(self, status: str):
        self.setProperty("cardStatus", status)
        self.update()

        for widget in [self.lbl_name, self.badge, self.status_dot]:
            widget.setProperty("cardStatus", status)
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    def update_state(self):
        if not self.session.is_installed:
            self.lbl_info.setText("Not detected on this system.")
            self.lbl_info.setToolTip("Plugin configuration could not be found.")
            self.badge.setText("NOT FOUND")

            self.toggle.blockSignals(True)
            self.toggle.setChecked(False)
            self.toggle.setEnabled(False)
            self.toggle.blockSignals(False)

            self.btn_auto.setVisible(True)
            self._apply_status("missing")

        elif not self.session.is_path_valid:
            self.lbl_info.setText(self._format_path(self.session.current_path))
            self.lbl_info.setToolTip(str(self.session.current_path))
            self.badge.setText("INVALID PATH")

            self.toggle.blockSignals(True)
            self.toggle.setChecked(False)
            self.toggle.setEnabled(False)
            self.toggle.blockSignals(False)

            self.btn_auto.setVisible(True)
            self._apply_status("error")

        else:
            self.lbl_info.setText(self._format_path(self.session.current_path))
            self.lbl_info.setToolTip(str(self.session.current_path))

            self.badge.setText("READY")

            self.toggle.blockSignals(True)
            self.toggle.setEnabled(True)
            self.toggle.setChecked(self.session.is_enabled)
            self.toggle.blockSignals(False)

            self.btn_auto.setVisible(True)
            self._apply_status("ready")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, f"Set Path for {self.session.name}")
        if folder: self.path_changed.emit(self.daw_id_str, folder)

    def set_loading(self, is_loading):
        self.loader.setVisible(is_loading)
        # Während des Scans beide Buttons ausblenden, danach beide wieder einblenden
        self.btn_auto.setVisible(not is_loading)
        self.btn_edit.setVisible(not is_loading)
        if is_loading:
            self.badge.setText("SCANNING...")
            self._apply_status("loading")

    def set_result(self, count):
        self.set_loading(False)
        self.badge.setText(f"+{count} FOUND")
        self._apply_status("ready")

    def on_toggle(self, state):
        self.session.is_enabled = (state == Qt.CheckState.Checked.value)

    def update_scan_progress(self, msg: str):
        short_msg = msg if len(msg) < 38 else msg[:35] + "..."
        self.lbl_info.setText(f"> {short_msg}")