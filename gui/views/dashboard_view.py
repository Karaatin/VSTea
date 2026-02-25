import platform
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QScrollArea, QMessageBox,
                               QGridLayout, QFrame, QLabel)
from PySide6.QtCore import Qt, QThreadPool, Signal

from core.enums import DawID
from core.scanners import ALL_SCANNERS
from gui.workers import DawScanWorker
from gui.widgets.daw_card import DawCardWidget
from gui.widgets.success_dialog import ScanSuccessDialog


class DashboardView(QWidget):
    scan_completed = Signal()

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.thread_pool = QThreadPool.globalInstance()
        self.active_workers = 0
        self.daw_widgets = {}

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 60, 50)
        layout.setSpacing(20)

        layout.addWidget(self._create_header())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setObjectName("TransparentScroll")

        grid_container = QWidget()
        self.grid = QGridLayout(grid_container)
        self.grid.setSpacing(20)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)

        row, col, max_cols = 0, 0, 3
        sorted_sessions = sorted(self.controller.sessions.values(), key=lambda s: not s.is_installed)

        for session in sorted_sessions:
            card = DawCardWidget(session)
            card.path_changed.connect(self.on_path_changed)
            card.auto_detect_requested.connect(self.on_auto_detect)

            card.toggle.stateChanged.connect(self.update_dashboard_stats)

            self.daw_widgets[session.id.value] = card
            self.grid.addWidget(card, row, col)

            col += 1
            if col >= max_cols: col = 0; row += 1

        scroll.setWidget(grid_container)
        layout.addWidget(scroll)

        layout.addWidget(self._create_footer())

        self.update_dashboard_stats()

    def _create_header(self):
        header_container = QWidget()
        h_layout = QHBoxLayout(header_container)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.setSpacing(15)

        self.sys_pill = QFrame()
        self.sys_pill.setObjectName("HeaderPill")
        sys_layout = QHBoxLayout(self.sys_pill)
        sys_layout.setContentsMargins(16, 10, 16, 10)

        sys_name = platform.system()
        sys_rel = platform.release()

        self.lbl_sys = QLabel(f"{sys_name} {sys_rel}")
        self.lbl_sys.setObjectName("HeaderStat")
        sys_layout.addWidget(self.lbl_sys)

        self.daw_pill = QFrame()
        self.daw_pill.setObjectName("HeaderPill")
        daw_layout = QHBoxLayout(self.daw_pill)
        daw_layout.setContentsMargins(16, 10, 16, 10)

        self.lbl_daw_stat = QLabel("DAW Status: 0 of 0 configured")
        self.lbl_daw_stat.setObjectName("HeaderStat")
        daw_layout.addWidget(self.lbl_daw_stat)

        h_layout.addWidget(self.sys_pill)
        h_layout.addStretch()
        h_layout.addWidget(self.daw_pill)

        return header_container

    def _create_footer(self):
        footer = QFrame()
        footer.setObjectName("DashboardFooter")
        f_layout = QHBoxLayout(footer)
        f_layout.setContentsMargins(10, 15, 10, 0)

        self.lbl_footer_info = QLabel("Ready to scan 0 DAWs. This might take a few seconds.")
        self.lbl_footer_info.setObjectName("FooterInfo")

        f_layout.addWidget(self.lbl_footer_info)
        f_layout.addStretch()

        self.btn_scan = QPushButton("Start Inventory Scan")
        self.btn_scan.setObjectName("ScanBtn")  # Ein eigener, schlankerer Button!
        self.btn_scan.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_scan.clicked.connect(self.start_scan)
        f_layout.addWidget(self.btn_scan)

        return footer

    def update_dashboard_stats(self, *args):
        total_daws = len(self.controller.sessions)
        installed_daws = sum(1 for s in self.controller.sessions.values() if s.is_installed)
        active_daws = sum(1 for s in self.controller.sessions.values() if s.is_installed and s.is_enabled)

        self.lbl_daw_stat.setText(f"DAW Status: {installed_daws} of {total_daws} configured")

        if active_daws > 0:
            self.lbl_footer_info.setText(f"Ready to scan {active_daws} DAWs. This might take a few seconds.")
            self.btn_scan.setEnabled(True)
        else:
            self.lbl_footer_info.setText("No DAWs selected for scanning.")
            self.btn_scan.setEnabled(False)

    def on_path_changed(self, daw_id_str, new_path):
        try:
            daw_id = DawID(daw_id_str)
            is_valid = self.controller.update_path(daw_id, new_path)

            if is_valid:
                self.controller.sessions[daw_id].is_enabled = True
                self.controller.sessions[daw_id].is_installed = True
            else:
                self.controller.sessions[daw_id].is_enabled = False
                QMessageBox.warning(
                    self,
                    "Invalid path",
                    f"The selected folder does not appear to contain valid configuration files for {self.controller.sessions[daw_id].name}."
                )

            self.daw_widgets[daw_id_str].update_state()
            self.update_dashboard_stats()
        except ValueError:
            pass

    def on_auto_detect(self, daw_id_str):
        try:
            daw_id = DawID(daw_id_str)
            scanner = next((s for s in ALL_SCANNERS if s.id == daw_id), None)
            if scanner:
                path = scanner.find_path(self.controller.system)
                if path:
                    self.controller.update_path(daw_id, path)
                    self.controller.sessions[daw_id].is_installed = True
                    self.controller.sessions[daw_id].is_enabled = True
                else:
                    self.controller.sessions[daw_id].is_installed = False
                    self.controller.sessions[daw_id].is_enabled = False
                    QMessageBox.information(
                        self,
                        "Auto-Detect",
                        f"Could not find default path for {daw_id.value}."
                    )

                self.daw_widgets[daw_id_str].update_state()
                self.update_dashboard_stats()  # Update Header/Footer
        except Exception:
            pass

    def start_scan(self):
        active_sessions = [
            sess for sess in self.controller.sessions.values()
            if sess.is_enabled and sess.is_installed
        ]

        if not active_sessions:
            return

        self.btn_scan.setEnabled(False)
        self.btn_scan.setText("⏳ Scanning...")
        self.lbl_footer_info.setText("Scan in progress. Please wait while we gather your plugins...")

        self.controller.merger.clear()
        self.active_workers = len(active_sessions)

        for session in active_sessions:
            daw_id_str = session.id.value
            if daw_id_str in self.daw_widgets:
                self.daw_widgets[daw_id_str].set_loading(True)

            worker = DawScanWorker(daw_id_str, session)
            worker.signals.progress.connect(self._on_worker_progress)
            worker.signals.finished.connect(self._on_worker_finished)
            worker.signals.error.connect(self._on_worker_error)
            self.thread_pool.start(worker)

    def _on_worker_progress(self, daw_id_str, msg):
        if daw_id_str in self.daw_widgets:
            self.daw_widgets[daw_id_str].update_scan_progress(msg)

    def _on_worker_finished(self, daw_id_str, plugins):
        if daw_id_str in self.daw_widgets:
            self.daw_widgets[daw_id_str].set_result(len(plugins))
        self.controller.merger.merge_list(plugins)

        self.active_workers -= 1
        if self.active_workers == 0:
            self._on_all_scans_completed()

    def _on_worker_error(self, daw_id_str, error_msg):
        if daw_id_str in self.daw_widgets:
            self.daw_widgets[daw_id_str].lbl_info.setText("Error during scan!")
            self.daw_widgets[daw_id_str].set_loading(False)

        self.active_workers -= 1
        if self.active_workers == 0:
            self._on_all_scans_completed()

    def _on_all_scans_completed(self):
        final_library = self.controller.merger.get_sorted_library()
        self.btn_scan.setEnabled(True)
        self.btn_scan.setText("Start Inventory Scan")
        self.update_dashboard_stats()

        dimmer = QWidget(self.window())
        dimmer.setObjectName("DimmerOverlay")
        dimmer.setGeometry(self.window().rect())
        dimmer.show()

        dialog = ScanSuccessDialog(self.window(), len(final_library))
        dialog.exec()

        dimmer.deleteLater()
        self.scan_completed.emit()