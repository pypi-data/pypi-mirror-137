from dataclasses import dataclass
from .utils import ResponseResourceBase

@dataclass
class ThumbnailKey:
    url: str = None
    width: int = None
    height: int = None

@dataclass
class ThumbnailResource:
    default: ThumbnailKey = None
    medium: ThumbnailKey = None
    high: ThumbnailKey = None
    standard: ThumbnailKey = None
    maxres: ThumbnailKey = None

@dataclass  
class ThumbnailSetResponse(ResponseResourceBase):
    items: list[ThumbnailResource] = None
