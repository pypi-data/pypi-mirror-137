"""Class representations of the `Playlist` resource."""

from dataclasses import dataclass
from .utils import ResponseResourceBase, create_list_response
from .ThumbnailResources import ThumbnailResource

@dataclass
class Localized:
    title: str = None
    description: str = None
    
@dataclass
class Snippet:
    published_at: str = None
    channel_id: str = None
    title: str = None
    description: str = None
    thumbnails: ThumbnailResource = None
    channel_title: str = None
    default_language: str = None
    localized: Localized = Localized()
    
@dataclass
class Status:
    privacy_status: str = None
    
@dataclass
class ContentDetails:
    item_count: int = None
    
@dataclass
class Player:
    embed_html: str = None

@dataclass
class PlaylistResource(ResponseResourceBase):
    """
    The class representation for the `Playlist` JSON resource during request bodies and responses.
    """    
    id: str = None
    
    content_details: ContentDetails = None
    player: Player = None 
    snippet: Snippet = Snippet()
    status: Status = Status()

class PlaylistListResponse(create_list_response(PlaylistResource)):
    """The class representation of playlistListResponse resource."""
