from pathlib import Path

from core.config import ConfigManager
from core.environment import Environment
from core.enums import DawID
from core.merger import PluginMerger

from core.scanners import ALL_SCANNERS

from core.parsers import (
    FLStudioParser,
    ReaperParser,
    AbletonParser,
    BitwigParser,
    CubaseParser,
    LogicParser,
    StudioOneParser,
)

class SessionConfig:
    def __init__(self, daw_id: DawID, name: str, parser_class, path):
        self.id = daw_id
        self.name = name
        self.parser_class = parser_class
        self.current_path = path

        if path is None or not path.exists():
            self.is_installed = False
            self.is_path_valid = False
            self.is_enabled = False
        else:
            temp_parser = parser_class(path)

            if hasattr(temp_parser, 'is_valid') and not temp_parser.is_valid():
                self.is_installed = False
                self.is_path_valid = False
                self.is_enabled = False
            else:
                # Alles perfekt!
                self.is_installed = True
                self.is_path_valid = True
                self.is_enabled = True

class WorkflowController:
    def __init__(self, progress_callback=None):

        if progress_callback:
            progress_callback("Loading Configuration...")

        self.config = ConfigManager()

        if progress_callback:
            progress_callback("Detecting System Environment...")

        self.system = Environment.detect()

        if progress_callback:
            progress_callback("Initializing Plugin Merger...")

        self.merger = PluginMerger()

        self.sessions = {}

        self._initialize_sessions(progress_callback)

        if progress_callback:
            progress_callback("Core Initialization Complete.")

    def _initialize_sessions(self, progress_callback=None):
        for scanner in ALL_SCANNERS:
            if progress_callback:
                progress_callback(f"Scanning default paths for {scanner.name}...")

            found_path = scanner.find_path(self.system)

            parser_cls = self._get_parser_class(scanner.id)

            session = SessionConfig(
                daw_id=scanner.id,
                name=scanner.name,
                parser_class=parser_cls,
                path=found_path
            )

            self.sessions[scanner.id] = session

    def _get_parser_class(self, daw_id: DawID):
        if daw_id == DawID.FL_STUDIO:  return FLStudioParser
        if daw_id == DawID.REAPER:     return ReaperParser
        if daw_id == DawID.ABLETON:    return AbletonParser
        if daw_id == DawID.BITWIG:     return BitwigParser
        if daw_id == DawID.CUBASE:     return CubaseParser
        if daw_id == DawID.LOGIC:      return LogicParser
        if daw_id == DawID.STUDIO_ONE: return StudioOneParser

        return None

    def update_path(self, daw_id: DawID, new_path_str: str) -> bool:
        if daw_id in self.sessions:
            p = Path(new_path_str)
            session = self.sessions[daw_id]

            if not p.exists():
                session.is_path_valid = False
                return False

            is_valid = False

            temp_parser = session.parser_class(p)

            if hasattr(temp_parser, 'is_valid'):
                is_valid = temp_parser.is_valid()
            else:
                is_valid = any(p.iterdir())

            session.current_path = p
            session.is_path_valid = is_valid

            if is_valid:
                session.is_installed = True

            return is_valid

        return False