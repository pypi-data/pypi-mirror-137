from typing import Literal
from ..resources.VideoResources import VideoResource, VideoListResponse, VideoGetRatingResponse, VideoReportAbuseBody
from googleapiclient.discovery import Resource
from googleapiclient.http import MediaFileUpload

__VideoPartType = Literal[
    "content_details", "file_details",
    "live_streaming_details",
    "localizations", "player",
    "processing_details", "recording_details",
    "snippet", "statistics",
    "status", "suggestions",
    "topic_details"
]
VideoPartType = __VideoPartType | list[__VideoPartType]

class Video:
    def __init__(self, client: Resource) -> None:
        self.client: Resource = client
        
    def list(self, *, part: VideoPartType, chart: Literal["most_popular"] = None,
             id: str | list[str] = None, my_rating: Literal["like", "dislike"] = None,
             max_height: int = None, max_width: int = None, max_results: int = None,
             page_token: str = None, region_code: str = None, video_category_id: str = None,
             on_behalf_of_content_owner: str = None):
        """
        Return a list of videos items that match the parameters.
        For more info, visit\
[Google's official documentation](https://developers.google.com/youtube/v3/docs/playlistItems/list)
        """
        
        if len([x for x in (chart, id, my_rating) if x != None]) != 1: 
            raise Exception("No/too many filters specified.")
        
        if type(part) == list:
            part = ",".join(part)
        if type(id) == list:
            id = ",".join(id)
        
        req = self.client.videos()\
        .list(part=part, 
              chart=chart, id=id, myRating=my_rating, 
              maxHeight=max_height,maxWidth=max_width,maxResults=max_results,
              pageToken=page_token, regionCode=region_code, videoCategoryId=video_category_id,
              onBehalfOfContentOwner=on_behalf_of_content_owner, hl="es")
        
        return VideoListResponse._from_response_dict(req.execute())
        
    def insert(self, media_body: str, body: VideoResource = None,
               *, part: VideoPartType, notify_subscribers: bool = True,
               on_behalf_of_content_owner: str = None):
        """
        Uploads a video to YouTube and optionally sets the video's metadata.
        For more info, visit\
    [Google's official documentation](https://developers.google.com/youtube/v3/docs/playlists/insert)
        """
        request_body = {}
        if body:
            if 'snippet' in part:
                request_body["snippet"] = {
                    "title": body.snippet.title,
                    "description": body.snippet.description,
                    "tags": body.snippet.tags,
                    "categoryId": body.snippet.category_id,
                    "defaultLanguage": body.snippet.default_language
                }
            if 'status' in part:
                request_body['status'] = {
                    "embeddable": body.status.embeddable,
                    "license": body.status.license,
                    "privacyStatus": body.status.privacy_status,
                    "publicStatsViewable": body.status.public_stats_viewable,
                    "publishAt": body.status.publish_at,
                    "selfDeclaredMadeForKids": body.status.self_declared_made_for_kids,
                }
            if "recordingDetails" in part:
                request_body["recordingDetails"] = {
                    "recordingDate": body.recording_details.recording_date 
                }
        
        if type(part) == list:
            part = ",".join(part)
            
        req = self.client.videos().insert(part=part, body = request_body, 
                                          media_body=MediaFileUpload(media_body),
                                          notifySubscribers=notify_subscribers,
                                          onBehalfOfContentOwner=on_behalf_of_content_owner)
        
        return VideoResource._from_response_dict(req.execute())
    
    def update(self, body: VideoResource, *, part: VideoPartType,
               on_behalf_of_content_owner: str = None):
        """
        Updates a video's metadata.
        For more info, visit\
    [Google's official documentation](https://developers.google.com/youtube/v3/docs/playlists/insert)
        """
        request_body = {
            "id": body.id
        }
        if body:
            if 'snippet' in part:
                request_body["snippet"] = {
                    "title": body.snippet.title,
                    "description": body.snippet.description,
                    "tags": body.snippet.tags,
                    "categoryId": body.snippet.category_id,
                    "defaultLanguage": body.snippet.default_language
                }
            if 'status' in part:
                request_body['status'] = {
                    "embeddable": body.status.embeddable,
                    "license": body.status.license,
                    "privacyStatus": body.status.privacy_status,
                    "publicStatsViewable": body.status.public_stats_viewable,
                    "publishAt": body.status.publish_at,
                    "selfDeclaredMadeForKids": body.status.self_declared_made_for_kids,
                }
            if "recordingDetails" in part:
                request_body["recordingDetails"] = {
                    "recordingDate": body.recording_details.recording_date 
                }
                
        if type(part) == list:
            part = ",".join(part)
            
        req = self.client.videos().update(part=part, body=request_body,
                                          onBehalfOfContentOwner=on_behalf_of_content_owner)
        return VideoResource._from_response_dict(req.execute())
    
    def delete(self, video_id: str,
               on_behalf_of_content_owner: str = None):
        """
        Deletes a video.
        For more info, visit\
    [Google's official documentation](https://developers.google.com/youtube/v3/docs/playlists/delete)
        """
        request = self.client.videos().delete(
            id=video_id,
            onBehalfOfContentOwner=on_behalf_of_content_owner
        )
        request.execute()
    
    def rate(self, video_id: str, rating: Literal['dislike', 'like', 'none']):
        """
        Like, dislike, or remove your rAting from the video.
        For more info, visit\
    [Google's official documentation](https://developers.google.com/youtube/v3/docs/playlists/insert)
        """
        
        req = self.client.videos().rate(id=video_id, rating=rating)
        req.execute()
        
    def get_rating(self, video_id: str,
                   on_behalf_of_content_owner: str = None):
        res = self.client.videos().getRating(
            id=video_id,
            onBehalfOfContentOwner=on_behalf_of_content_owner
            ).execute()
        return VideoGetRatingResponse._from_response_dict(res)
    
    def report_abuse(self, body: VideoReportAbuseBody):
        request_body = {
            "videoId": body.video_id,
            "reasonId": body.reason_id,
            "secondaryReasonId": body.secondary_reason_id,
            "comments": body.comments,
            "language": body.language,
        }
        self.client.videos().reportAbuse(body=request_body)
