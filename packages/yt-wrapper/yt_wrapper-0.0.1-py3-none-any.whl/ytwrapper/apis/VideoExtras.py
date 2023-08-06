from ..resources.VideoExtraResources import VideoCategoryListResponse, VideoAbuseReportReasonListResponse
from googleapiclient.discovery import Resource

class VideoCategory:
    def __init__(self, client: Resource) -> None:
        self.client: Resource = client
        
    def list(self, *, id: str|list[str] = None, region_code: str = None):
        if type(id) == list:
            id = ",".join(id)
        
        req = self.client.videoCategories().list(id=id, part='snippet', regionCode=region_code)
        return VideoCategoryListResponse._from_response_dict(req.execute())
        ...

class VideoAbuseReportReason:
    def __init__(self, client: Resource) -> None:
        self.client: Resource = client
        
    def list(self):
        req = self.client.videoAbuseReportReasons().list(part='snippet')
        return VideoAbuseReportReasonListResponse._from_response_dict(req.execute())
        ...