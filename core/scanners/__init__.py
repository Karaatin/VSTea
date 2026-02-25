from .ableton import AbletonScanner
from .bitwig import BitwigScanner
from .cubase import CubaseScanner
from .flstudio import FLStudioScanner
from .logic import LogicScanner
from .reaper import ReaperScanner
from .studioone import StudioOneScanner

ALL_SCANNERS = [
    AbletonScanner(),
    BitwigScanner(),
    CubaseScanner(),
    FLStudioScanner(),
    LogicScanner(),
    ReaperScanner(),
    StudioOneScanner(),
]