from pathlib import Path
from core.enums import DawID, OSType
from .base_scanner import DawScanner

class FLStudioScanner(DawScanner):
    def __init__(self):
        super().__init__(DawID.FL_STUDIO)

    def find_path(self, sys):
        candidates = []

        if sys.os_type == OSType.WINDOWS:
            reg_val = self._get_win_reg(r"Software\Image-Line\Shared\Paths", "Shared Data")
            if reg_val:
                base = Path(reg_val)
                candidates.append(base / "FL Studio" / "Presets" / "Plugin database" / "Installed")
                candidates.append(base / "Presets" / "Plugin database" / "Installed")

        docs = sys.documents / "Image-Line"
        candidates.append(docs / "FL Studio" / "Presets" / "Plugin database" / "Installed")
        candidates.append(docs / "Data" / "FL Studio" / "Presets" / "Plugin database" / "Installed")

        for p in candidates:
            if p.exists(): return p

        return None