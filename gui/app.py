import sys
import os
import traceback

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from PySide6.QtGui import QIcon
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QApplication

from gui.workers import InitWorker
from gui.styles import build_stylesheet
from gui.views.splash_view import ModernSplashScreen
from gui.views.main_view import MainWindow
from core.config import ConfigManager
from core.utils import resource_path

class AppLauncher(QObject):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.splash = ModernSplashScreen()
        self.splash.show()

        self.thread = QThread()
        self.worker = InitWorker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_init_finished)
        self.worker.progress.connect(self.update_splash_msg)
        self.worker.error.connect(self.on_error)

        self.thread.start()

    def update_splash_msg(self, msg):
        self.splash.show_message(msg)

    def on_init_finished(self, controller):
        try:
            self.splash.close()
            self.thread.quit()

            self.main_window = MainWindow(controller)
            self.main_window.show()

        except Exception as e:
            self.error.emit(traceback.format_exc())

    def on_error(self, err_msg):
        print(err_msg)
        self.splash.close()
        self.thread.quit()
        sys.exit(1)


def main():
    try:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

        app = QApplication(sys.argv)
        icon_path = resource_path("assets/icon_nt_static.svg")
        app.setWindowIcon(QIcon(icon_path))

        temp_config = ConfigManager()
        theme_name = temp_config.get("theme", "matcha")

        try:
            theme_module = __import__(f"gui.themes.{theme_name}", fromlist=['COLORS'])
            colors = theme_module.COLORS
        except ImportError:
            from gui.themes.matcha import COLORS
            colors = COLORS

        app.setStyleSheet(build_stylesheet(colors))

        launcher = AppLauncher(app)

        sys.exit(app.exec())
    except Exception as e:
        print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()