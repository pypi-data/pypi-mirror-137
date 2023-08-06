"""Class representations of the `Search` resource."""

from dataclasses import dataclass
from .utils import ResponseResourceBase, create_list_response
from .ThumbnailResources import ThumbnailResource

@dataclass
class Id:
    kind: str = None
    video_id: str = None
    channel_id: str = None
    playlist_id: str = None
    
@dataclass
class Snippet:
    published_at: str = None
    channelId: str = None
    title: str = None
    description: str = None
    thumbnails: ThumbnailResource = None
    channel_title: str = None
    live_broadcast_content: str = None

@dataclass
class SearchResult(ResponseResourceBase):
    id: Id = None
    snippet: Snippet = None

@dataclass
class SearchListResponse(create_list_response(SearchResult)):
    """The class representation for the channelListResponse resource."""
    region_code: str = None
