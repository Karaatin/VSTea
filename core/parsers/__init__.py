from .ableton import AbletonParser
from .bitwig import BitwigParser
from .cubase import CubaseParser
from .flstudio import FLStudioParser
from .logic import LogicParser
from .reaper import ReaperParser
from .studioone import StudioOneParser

ALL_PARSERS = [
    AbletonParser,
    BitwigParser,
    CubaseParser,
    FLStudioParser,
    LogicParser,
    ReaperParser,
    StudioOneParser,
]