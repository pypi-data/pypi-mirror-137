from googleapiclient.discovery import Resource
from ..resources.ThumbnailResources import ThumbnailSetResponse
from googleapiclient.http import MediaFileUpload

class Thumbnail:
    def __init__(self, client: Resource) -> None:
        self.client = client
        
    def set(self, thumbnail_file: str, *, video_id: str,
             on_behalf_of_content_owner: str = None
            ):
        req = self.client.thumbnails().set(
            media_body=MediaFileUpload(thumbnail_file),
            videoId=video_id,
            onBehalfOfContentOwner=on_behalf_of_content_owner
        )
        
        return ThumbnailSetResponse._from_response_dict(req.execute())
        ...