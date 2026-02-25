from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QStackedWidget, QMessageBox)
from PySide6.QtCore import Qt, QUrl

from gui.widgets.sidebar import Sidebar
from gui.views.dashboard_view import DashboardView
from gui.views.results_view import ResultsView
from gui.views.settings_view import SettingsView
from gui.views.about_view import AboutView
from gui.workers import UpdateCheckWorker

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("VSTea")
        self.resize(1200, 800)
        self.setMinimumSize(950, 650)

        self.init_ui()

        self._start_update_check()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setCentralWidget(main_widget)

        self.sidebar = Sidebar()
        self.sidebar.nav_clicked.connect(self._set_active_nav)
        main_layout.addWidget(self.sidebar)

        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        top_bar = QWidget()
        top_bar.setFixedHeight(50)
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(20, 10, 20, 0)

        self.btn_toggle = QPushButton("☰")
        self.btn_toggle.setObjectName("ToggleBtn")
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.clicked.connect(self.sidebar.toggle)
        top_bar_layout.addWidget(self.btn_toggle)

        self.lbl_top_brand = QLabel("VSTea")
        self.lbl_top_brand.setObjectName("TopBrand")
        top_bar_layout.addWidget(self.lbl_top_brand)
        top_bar_layout.addStretch()
        content_layout.addWidget(top_bar)

        self.stack = QStackedWidget()
        self.stack.setObjectName("MainContainer")

        self.page_dashboard = DashboardView(self.controller)
        self.page_results = ResultsView(self.controller, lambda: self._set_active_nav(0))
        self.page_settings = SettingsView(self.controller.config)
        self.page_about = AboutView()

        self.page_dashboard.scan_completed.connect(self._on_scan_finished)

        self.stack.addWidget(self.page_dashboard)
        self.stack.addWidget(self.page_results)
        self.stack.addWidget(self.page_settings)
        self.stack.addWidget(self.page_about)

        content_layout.addWidget(self.stack)
        main_layout.addWidget(content_container)

        self._set_active_nav(0)

    def _set_active_nav(self, target_index):
        self.stack.setCurrentIndex(target_index)
        self.sidebar.set_active(target_index)

    def _on_scan_finished(self):
        self.page_results.update_results()
        self._set_active_nav(1)

    def _start_update_check(self):
        # Wir fragen die Config ab (aus der settings_view.py)
        if self.controller.config.get("auto_updates", True):
            self.update_worker = UpdateCheckWorker()
            self.update_worker.result.connect(self._on_update_check_result)
            self.update_worker.start()

    def _on_update_check_result(self, has_update: bool, new_version: str, url: str):
        if has_update:
            from core.constants import APP_VERSION

            msg = QMessageBox(self)
            msg.setWindowTitle("Update Available")
            msg.setText(
                f"A new version of VSTea ({new_version}) is available!\nYou are currently running version {APP_VERSION}.")
            msg.setInformativeText("Would you like to download the update now?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setDefaultButton(QMessageBox.StandardButton.Yes)

            if msg.exec() == QMessageBox.StandardButton.Yes:
                QDesktopServices.openUrl(QUrl(url))