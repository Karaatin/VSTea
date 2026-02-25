from abc import ABC, abstractmethod
from pathlib import Path
from core.enums import DawID

try:
    import winreg
except ImportError:
    winreg = None

class DawScanner(ABC):
    def __init__(self, daw_id: DawID):
        self.id = daw_id
        self.name = daw_id.value

    @abstractmethod
    def find_path(self, system_info) -> Path | None:
        pass

    def _get_win_reg(self, key_path, value_name):
        if not winreg: return None
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
            val, _ = winreg.QueryValueEx(reg_key, value_name)
            winreg.CloseKey(reg_key)
            return val
        except Exception:
            return None