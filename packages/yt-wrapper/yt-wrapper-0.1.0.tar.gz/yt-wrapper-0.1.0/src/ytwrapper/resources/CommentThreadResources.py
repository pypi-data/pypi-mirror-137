"""Class representations of the `CommentThread` resource."""

from dataclasses import dataclass
from .utils import ResponseResourceBase, create_list_response
from .CommentResources import CommentResource

@dataclass
class Snippet:
    channel_id: str = None
    video_id: str = None
    top_level_comment: CommentResource = CommentResource()
    can_reply: bool = None
    total_reply_count: int = None 
    is_public: bool = None
    
@dataclass
class Replies:
    comments: list[CommentResource] = None
    
@dataclass
class CommentThreadResource(ResponseResourceBase):
    id: str = None
    snippet: Snippet = Snippet()
    replies: Replies = None

class CommentThreadListResponse(create_list_response(CommentThreadResource)):
    """The class representation for the commentThreadListResponse resource."""
