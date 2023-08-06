"""Class representations of the `Subscription` resource."""

from dataclasses import dataclass
from .utils import ResponseResourceBase, create_list_response
from .ThumbnailResources import ThumbnailKey

@dataclass
class Thumbnails:
    default: ThumbnailKey = None
    medium: ThumbnailKey = None
    high: ThumbnailKey = None

@dataclass
class ResourceId:
    kind: str = None
    channel_id: str = None

@dataclass
class Snippet:
    published_at: str = None
    channel_title: str = None
    title: str = None
    description: str = None
    channel_id: str = None
    thumbnails: Thumbnails = None

@dataclass
class ContentDetails:
    total_item_count: int = None
    new_item_count: int = None
    activity_type: str = None

@dataclass
class SubscriberSnippet:
    title: str = None
    description: str = None
    channel_id: str = None
    thumbnails: Thumbnails = None
    
@dataclass
class SubscriptionResource(ResponseResourceBase):
    id: str = None
    content_details: ContentDetails = None
    subscriber_snippet: SubscriberSnippet = None
    snippet: Snippet = Snippet()

@dataclass
class SubscriptionListResponse(create_list_response(SubscriptionResource)):
    pass
