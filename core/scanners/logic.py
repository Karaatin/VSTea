from core.enums import DawID, OSType
from .base_scanner import DawScanner

class LogicScanner(DawScanner):
    def __init__(self):
        super().__init__(DawID.LOGIC)

    def find_path(self, sys):
        candidates = []

        if sys.os_type == OSType.MACOS:
            candidates.append(sys.user_home / "Music" / "Audio Music Apps" / "Plug-In Settings")

        for p in candidates:
            if p.exists():
                return p

        return None