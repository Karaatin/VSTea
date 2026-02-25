import traceback
from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QThread

from core.controller import WorkflowController
from core.utils import check_for_updates

class InitWorker(QObject):
    finished = Signal(object)
    progress = Signal(str)
    error = Signal(str)

    def run(self):
        try:
            controller = WorkflowController(progress_callback=self.progress.emit)
            self.finished.emit(controller)

        except Exception as e:
            err_msg = traceback.format_exc()
            self.error.emit(err_msg)

class UpdateCheckWorker(QThread):
    result = Signal(bool, str, str)

    def run(self):
        has_update, new_version, url = check_for_updates()
        self.result.emit(has_update, new_version or "", url or "")

class WorkerSignals(QObject):
    started = Signal(str)
    progress = Signal(str, str)
    finished = Signal(str, list)
    error = Signal(str, str)

class DawScanWorker(QRunnable):
    def __init__(self, daw_id_str: str, session_config):
        super().__init__()
        self.daw_id_str = daw_id_str
        self.session = session_config
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            self.signals.started.emit(self.daw_id_str)
            self.signals.progress.emit(self.daw_id_str, "Initializing parser...")

            parser = self.session.parser_class(self.session.current_path)

            def progress_callback(msg: str):
                self.signals.progress.emit(self.daw_id_str, msg)

            self.signals.progress.emit(self.daw_id_str, "Scanning plugin directories...")

            plugins = parser.parse(progress_callback=progress_callback)

            self.signals.progress.emit(self.daw_id_str, "Finalizing results...")
            self.signals.finished.emit(self.daw_id_str, plugins)

        except Exception:
            self.signals.error.emit(self.daw_id_str, traceback.format_exc())