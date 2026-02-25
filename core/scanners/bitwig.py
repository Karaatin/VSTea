from core.enums import DawID, OSType
from .base_scanner import DawScanner

class BitwigScanner(DawScanner):
    def __init__(self):
        super().__init__(DawID.BITWIG)

    def find_path(self, sys):
        candidates = []

        if sys.os_type == OSType.WINDOWS:
            candidates.append(sys.local_path / "Bitwig Studio")

        elif sys.os_type == OSType.MACOS:
            candidates.append(sys.config_path / "Bitwig" / "Bitwig Studio")

        elif sys.os_type == OSType.LINUX:
            candidates.append(sys.user_home / ".BitwigStudio")

        for p in candidates:
            if p.exists():
                return p

        return None