import xml.etree.ElementTree as ET
from typing import List, Callable, Optional
from .base_parser import BaseParser
from core.plugin_model import Plugin
from core.enums import PluginFormat

class CubaseParser(BaseParser):
    def is_valid(self) -> bool:
        if not self.config_path.is_dir():
            return False

        targets = ["Vst2xPluginInfos.xml", "VstPlugInfoV3.xml", "Vst2xPlugins.xml"]
        return any((self.config_path / t).exists() for t in targets)

    def parse(self, progress_callback: Optional[Callable[[str], None]] = None) -> List[Plugin]:
        plugins = []
        targets = ["Vst2xPluginInfos.xml", "VstPlugInfoV3.xml", "Vst2xPlugins.xml"]

        for xml_name in targets:
            xml_path = self.config_path / xml_name
            if not xml_path.exists(): continue

            if progress_callback:
                progress_callback(f"Reading {xml_name}...")

            try:
                tree = ET.parse(xml_path)
                root = tree.getroot()

                for item in root.iter("item"):
                    name = None
                    vendor = "Unknown"
                    path = ""
                    cid = ""

                    for child in item:
                        key = child.get("name")
                        val = child.get("value") or child.text

                        if key == "Name":
                            name = val
                        elif key == "Vendor":
                            vendor = val
                        elif key == "Path":
                            path = val
                        elif key == "cid":
                            cid = val

                    if name:
                        if "VstPlugInfoV3" in xml_name:
                            fmt = PluginFormat.VST3.value
                        elif "Vst2" in xml_name:
                            fmt = PluginFormat.VST2.value
                        else:
                            fmt = PluginFormat.UNKNOWN.value

                        p = Plugin(
                            name=name,
                            vendor=vendor if vendor else "Unknown",
                            formats={fmt},
                            detected_by={"Cubase"},
                            instances=[{"daw": "Cubase", "format": fmt, "path": path}]
                        )
                        plugins.append(p)
            except Exception as e:
                pass

        return plugins