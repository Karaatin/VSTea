import plistlib
from pathlib import Path
from typing import List, Callable, Optional

from .base_parser import BaseParser
from core.plugin_model import Plugin
from core.enums import PluginFormat

class LogicParser(BaseParser):

    @property
    def global_au_paths(self):
        return [
            Path("/Library/Audio/Plug-Ins/Components"),
            Path.home() / "Library/Audio/Plug-Ins/Components"
        ]

    def is_valid(self) -> bool:
        if not self.config_path or not self.config_path.exists():
            return False
        return any(p.exists() for p in self.global_au_paths)

    def parse(self, progress_callback: Optional[Callable[[str], None]] = None) -> List[Plugin]:
        if not self.is_valid():
            return []

        plugins = []
        if progress_callback:
            progress_callback("Scanning macOS Audio Units for Logic Pro...")

        for au_dir in self.global_au_paths:
            if not au_dir.exists():
                continue

            for item in au_dir.iterdir():
                if item.is_dir() and item.suffix == ".component":
                    plist_path = item / "Contents" / "Info.plist"

                    if plist_path.exists():
                        try:
                            with open(plist_path, 'rb') as f:
                                plist_data = plistlib.load(f)

                            name = None
                            vendor = "Unknown"

                            audio_components = plist_data.get("AudioComponents", [])
                            if audio_components and isinstance(audio_components, list):
                                first_comp = audio_components[0]
                                au_name_string = first_comp.get("name", "")

                                if ":" in au_name_string:
                                    vendor_part, name_part = au_name_string.split(":", 1)
                                    vendor = vendor_part.strip()
                                    name = name_part.strip()
                                elif au_name_string:
                                    name = au_name_string.strip()

                            if not name:
                                name = (plist_data.get("CFBundleDisplayName") or
                                        plist_data.get("CFBundleName") or
                                        plist_data.get("CFBundleExecutable") or
                                        item.stem)

                            if vendor == "Unknown":
                                identifier = plist_data.get("CFBundleIdentifier", "")
                                if identifier:
                                    parts = identifier.split('.')
                                    if len(parts) >= 2:
                                        if parts[1].lower() in ["co", "com", "org", "net", "uk", "se", "de"] and len(
                                                parts) > 2:
                                            vendor = parts[2].capitalize()
                                        else:
                                            vendor = parts[1].capitalize()

                            fmt = PluginFormat.STOCK.value if vendor.lower() == "apple" else PluginFormat.AU.value

                            p = Plugin(
                                name=name,
                                vendor=vendor,
                                formats={fmt},
                                detected_by={"Logic Pro"},
                                instances=[{"daw": "Logic Pro", "format": fmt, "path": str(item)}]
                            )
                            plugins.append(p)

                        except Exception:
                            pass

        return plugins