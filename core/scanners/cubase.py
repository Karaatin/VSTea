from core.enums import DawID, OSType
from .base_scanner import DawScanner

class CubaseScanner(DawScanner):
    def __init__(self):
        super().__init__(DawID.CUBASE)

    def find_path(self, sys):
        candidates = []

        if sys.os_type == OSType.WINDOWS:
            candidates.append(sys.config_path / "Steinberg")

        elif sys.os_type == OSType.MACOS:
            candidates.append(sys.user_home / "Library" / "Preferences")

        for p in candidates:
            if p.exists():
                has_cubase = any("Cubase" in child.name for child in p.iterdir() if child.is_dir())
                if has_cubase:
                    return p

        return None