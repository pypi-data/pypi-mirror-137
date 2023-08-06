"""Class representations of the `ChannelSection` resource."""

from dataclasses import dataclass
from .utils import ResponseResourceBase

@dataclass
class Snippet:
    type: str = None
    channel_id: str = None
    title: str = None
    position: int = None
    
@dataclass
class ContentDetails:
    playlists: list[str] = None
    channels: list[str] = None
    
@dataclass
class ChannelSectionResource(ResponseResourceBase):
    id: str = None
    content_details: ContentDetails = ContentDetails()
    snippet: Snippet = Snippet()
    
@dataclass
class ChannelSectionListResponse(ResponseResourceBase):
    items: list[ChannelSectionResource] = None