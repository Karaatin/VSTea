from pathlib import Path
from core.enums import DawID, OSType
from .base_scanner import DawScanner

class ReaperScanner(DawScanner):
    def __init__(self):
        super().__init__(DawID.REAPER)

    def find_path(self, sys):
        candidates = []

        if sys.os_type == OSType.WINDOWS:
            candidates.append(sys.config_path / "REAPER")

            install_path_str = self._get_win_reg(r"Software\Cockos\REAPER", "InstallPath")
            if install_path_str:
                candidates.append(Path(install_path_str))

        elif sys.os_type == OSType.MACOS:
            candidates.append(sys.config_path / "REAPER")

        elif sys.os_type == OSType.LINUX:
            candidates.append(sys.config_path / "REAPER")

        for p in candidates:
            if p.exists():
                return p

        return None