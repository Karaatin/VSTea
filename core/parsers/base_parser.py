from abc import ABC, abstractmethod
from typing import List, Callable, Optional
from pathlib import Path
from core.plugin_model import Plugin

class BaseParser(ABC):
    def __init__(self, config_path: Path):
        self.config_path = config_path

    @abstractmethod
    def parse(self, progress_callback: Optional[Callable[[str], None]] = None) -> List[Plugin]:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        pass