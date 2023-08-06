"""Class representations of the `Channel` resource."""

from dataclasses import dataclass
from .utils import ResponseResourceBase, create_list_response
from .ThumbnailResources import ThumbnailResource

@dataclass
class Localized:
    title: str = None
    description: str = None

@dataclass
class Snippet:
    title: str = None
    description: str = None
    custom_url: str = None
    published_at: str = None
    thumbnails: ThumbnailResource = None
    default_language: str = None
    country: str = None
    localized: Localized = None

@dataclass
class RelatedPlaylists:
    likes: str = None
    favorites: str = None
    uploads: str = None
    
@dataclass
class ContentDetails:
    related_playlists: RelatedPlaylists = None

@dataclass
class Statistics:
    viewCount: int = None
    subscriberCount: int = None
    hiddenSubscriberCount: bool = None
    videoCount: int = None

@dataclass
class TopicDetails:
    topic_ids: list[str] = None
    topic_categories: list[str] = None
    
@dataclass
class Status:
    privacy_status: str = None
    is_linked: bool = None
    long_uploads_status: str = None
    made_for_kids: bool = None
    self_declared_made_for_kids: bool = None

@dataclass
class BrandingSettingsChannel:
    title: str = None
    description: str = None
    keywords: str = None
    tracking_analytics_account_id: str = None
    moderate_comments: bool = None
    unsubscribed_trailer: str = None
    default_language: str = None
    country: str = None
    
@dataclass
class Watch:
    text_color: str = None
    background_color: str = None
    featured_playlist_id: str = None

@dataclass
class BrandingSettings:
    channel: BrandingSettingsChannel = BrandingSettingsChannel()
    watch: Watch = None
    
@dataclass
class AuditDetails:
    overall_good_standing: bool = None
    community_guidelines_good_standing: bool = None
    copyright_strikes_good_standing: bool = None
    conten_id_claims_good_standing: bool = None
    
@dataclass
class ContentOwnerDetails:
    content_owner: str = None
    time_linked: str = None

@dataclass
class ChannelResource(ResponseResourceBase):
    id: str = None
    
    branding_settings: BrandingSettings = BrandingSettings()
    status: Status = Status()
    
    snippet: Snippet = None
    content_details: ContentDetails = None
    statistics: Statistics = None
    topic_details: TopicDetails = None
    status: Status = None
    audit_details: Snippet = None
    snippet: Snippet = None
    content_owner_details: ContentOwnerDetails = None

class ChannelListResponse(create_list_response(ChannelResource)):
    """The class representation for the channelListResponse resource."""

