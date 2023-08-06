"""Class representations of the `VideoCategory` and `VideoAbuseReportReason` resources."""

from dataclasses import dataclass
from .utils import ResponseResourceBase, create_list_response

@dataclass
class CategorySnippet:
    channel_id: str = 'UCBR8-60-B28hp2BmDPdntcQ'
    title: str = None
    assignable: bool = None
    
@dataclass
class VideoCategoryResource(ResponseResourceBase):
    id: str = None
    snippet: CategorySnippet = None
    
class VideoCategoryListResponse(create_list_response(VideoCategoryResource)):
    """The class representation for the videoCategoryListResponse resource."""

@dataclass
class SecondaryReasons:
    id: str = None
    label: str = None
    
@dataclass
class ReasonSnippet:
    label: str = None
    secondary_reasons: list[SecondaryReasons] = None
    
@dataclass
class VideoAbuseReportReasonResource(ResponseResourceBase):
    id: str = None
    snippet: ReasonSnippet = None

@dataclass
class VideoAbuseReportReasonListResponse(ResponseResourceBase):
    items: list[VideoAbuseReportReasonResource] = None