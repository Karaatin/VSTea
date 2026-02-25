import platform
import os
from pathlib import Path
from core.enums import OSType
from dataclasses import dataclass

@dataclass
class SystemInfo:
    os_type: OSType
    user_home: Path
    documents: Path
    config_path: Path
    local_path: Path

    @property
    def app_data(self): return self.config_path
    @property
    def local_app_data(self): return self.local_path

class Environment:

    @staticmethod
    def detect() -> SystemInfo:
        system_name = platform.system()
        user_home = Path.home()

        os_type = OSType.UNKNOWN
        documents = user_home / "Documents"
        config_path = user_home
        local_path = user_home

        if system_name == "Windows":
            os_type = OSType.WINDOWS
            roaming = os.environ.get('APPDATA')
            local = os.environ.get('LOCALAPPDATA')

            config_path = Path(roaming) if roaming else user_home
            local_path = Path(local) if local else user_home

            documents = user_home / "Documents"

        elif system_name == "Darwin":
            os_type = OSType.MACOS
            library = user_home / "Library"
            config_path = library / "Application Support"
            local_path = library / "Application Support"
            documents = user_home / "Documents"

        elif system_name == "Linux":
            os_type = OSType.LINUX
            config_path = Path(os.environ.get('XDG_CONFIG_HOME', user_home / ".config"))
            local_path = Path(os.environ.get('XDG_DATA_HOME', user_home / ".local" / "share"))
            documents = user_home / "Documents"

        return SystemInfo(
            os_type=os_type,
            user_home=user_home,
            documents=documents,
            config_path=config_path,
            local_path=local_path
        )