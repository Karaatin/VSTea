from pathlib import Path
from core.enums import DawID, OSType
from .base_scanner import DawScanner

class AbletonScanner(DawScanner):
    def __init__(self):
        super().__init__(DawID.ABLETON)

    def find_path(self, sys):
        candidates = []

        if sys.os_type == OSType.WINDOWS:
            candidates.append(Path.home() / "AppData" / "Local" / "Ableton" / "Live Database")

        elif sys.os_type == OSType.MACOS:
            candidates.append(Path.home() / "Library" / "Application Support" / "Ableton" / "Live Database")

        for p in candidates:
            if p.exists():
                return p

        return None