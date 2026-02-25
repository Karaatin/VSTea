from gui.themes import AVAILABLE_THEMES
import importlib
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QComboBox, QApplication

class SettingsView(QWidget):
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager

        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 50, 60, 50)
        layout.setSpacing(20)

        h1 = QLabel("Settings", objectName="H1")
        sub = QLabel("Customize your VSTea experience.", objectName="Sub")

        layout.addWidget(h1)
        layout.addWidget(sub)
        layout.addSpacing(20)

        self.chk_updates = QCheckBox("Enable Automatic Updates (OS based)")
        self.chk_updates.setChecked(self.config.get("auto_updates", True))
        self.chk_updates.stateChanged.connect(self._on_update_toggled)
        layout.addWidget(self.chk_updates)

        layout.addSpacing(20)
        lbl_theme = QLabel("Application Theme", objectName="H2")
        self.combo_theme = QComboBox()
        self.combo_theme.setFixedWidth(250)

        self.theme_ids = list(AVAILABLE_THEMES.keys())
        theme_names = list(AVAILABLE_THEMES.values())

        self.combo_theme.addItems(theme_names)

        current_theme = self.config.get("theme", "matcha")
        if current_theme in self.theme_ids:
            self.combo_theme.setCurrentIndex(self.theme_ids.index(current_theme))
        else:
            self.combo_theme.setCurrentIndex(0)

        self.combo_theme.currentIndexChanged.connect(self._on_theme_changed)

        layout.addWidget(lbl_theme)
        layout.addWidget(self.combo_theme)
        layout.addStretch()

    def _on_update_toggled(self, state):
        is_checked = (state == 2)
        self.config.set("auto_updates", is_checked)

    def _on_theme_changed(self, index):
        new_theme_name = self.theme_ids[index]
        self.config.set("theme", new_theme_name)

        try:
            importlib.invalidate_caches()
            theme_module = importlib.import_module(f"gui.themes.{new_theme_name}")
            from gui.styles import build_stylesheet

            app = QApplication.instance()
            if app:
                app.setStyleSheet(build_stylesheet(theme_module.COLORS))

        except Exception as e:
            pass