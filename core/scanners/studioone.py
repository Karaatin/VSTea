from core.enums import DawID, OSType
from .base_scanner import DawScanner

class StudioOneScanner(DawScanner):
    def __init__(self):
        super().__init__(DawID.STUDIO_ONE)

    def find_path(self, sys):
        candidates = []

        if sys.os_type == OSType.WINDOWS:
            candidates.append(sys.config_path / "PreSonus" / "Studio One 6")
            candidates.append(sys.config_path / "PreSonus" / "Studio One 5")
            candidates.append(sys.documents / "Studio One" / "Presets")

        elif sys.os_type == OSType.MACOS:
            candidates.append(sys.user_home / "Library" / "Application Support" / "PreSonus" / "Studio One 6")
            candidates.append(sys.documents / "Studio One" / "Presets")

        for p in candidates:
            if p.exists():
                return p

        return None