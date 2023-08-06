"""Class representations of the `I18nLanguage` and `I18nRegion` resources."""

from dataclasses import dataclass
from .utils import ResponseResourceBase

@dataclass
class LanguageSnippet:
    hl: str = None
    name: str = None

@dataclass
class RegionSnippet:
    gl: str = None
    name: str = None
    
@dataclass
class I18nLanguageResource(ResponseResourceBase):
    id: str = None
    snippet: LanguageSnippet = LanguageSnippet()
    
@dataclass
class I18nRegionResource(ResponseResourceBase):
    id: str = None
    snippet: RegionSnippet = RegionSnippet()

@dataclass
class I18nLanguageListResponse(ResponseResourceBase):
    items: list[I18nLanguageResource] = None
    
@dataclass
class I18nRegionListResponse(ResponseResourceBase):
    items: list[I18nRegionResource] = None



