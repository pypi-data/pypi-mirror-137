"""Class representations of the `Comment` resource."""

from dataclasses import dataclass
from .utils import ResponseResourceBase, create_list_response

@dataclass
class AuthorChannelId:
    value: str = None

@dataclass
class Snippet:
    author_display_name: str = None
    author_profile_image_url: str = None
    author_channel_url: str = None
    author_channel_id: AuthorChannelId = None
    channel_id: str = None
    video_id: str = None
    text_display: str = None
    text_original: str = None
    parent_id: str = None
    can_rate: bool = None
    viewer_rating: str = None
    like_count: int = None
    moderation_status: str = None
    published_at: str = None
    updated_at: str = None

@dataclass
class CommentResource(ResponseResourceBase):
    id: str = None
    snippet: Snippet = Snippet()

class CommentListResponse(create_list_response(CommentResource)):
    """The class representation for the commentListResponse resource."""
