"""Class representations of the `PlaylistItem` resource."""

from dataclasses import dataclass
from .utils import ResponseResourceBase, create_list_response
from .ThumbnailResources import ThumbnailResource

@dataclass
class ResourceId:
    kind: str = None
    video_id: str = None

@dataclass
class Snippet:
    published_at: str = None
    channel_id: str = None
    title: str = None
    description: str = None
    thumbnails: ThumbnailResource = None
    channel_title: str = None
    video_owner_channel_title: str = None
    video_owner_channel_id: str = None
    playlist_id: str = None
    position: int = None
    resource_id: ResourceId = ResourceId()

@dataclass
class ContentDetails:
    video_id: str = None
    note: str = None
    video_published_at: str = None
    
@dataclass
class Status:
    privacy_status: str = None
    
@dataclass
class PlaylistItemResource(ResponseResourceBase):
    id: str = None
    
    snippet: Snippet = Snippet()
    content_details: ContentDetails = ContentDetails()
    status: Status = None
    
class PlaylistItemListResponse(create_list_response(PlaylistItemResource)):
    """The class representation for the playlistItemListResponse resource."""
