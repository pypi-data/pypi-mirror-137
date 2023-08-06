from typing import Literal
from ..resources.SearchResultResources import SearchListResponse
from googleapiclient.discovery import Resource

class Search:
    def __init__(self, client: Resource) -> None:
        self.client: Resource = client
    # That's a lot of parameters!
    # With the amount of params this has, and the fact that I don't have a proper testing mechanism
    # and the fact that this uses a _lot_ of quota per call and I have the free tier of quota
    # means that a lot of the params here isn't gonna be tested. So yeah... 
    def list(self, q: str, *, for_content_owner: bool = None, for_developer: bool = None, for_mine: bool = None, related_to_video_id: bool = None,
             order: Literal['date', 'rating', 'relevance', 'title', 'videoCount', 'viewCount'] = None,
             safe_search: Literal['none', 'moderate', 'strict'] = None,
             type: Literal['channel', 'playlist', 'video'] = None, topic_id: str = None, 
             published_atfer: str = None, publised_before: str = None,
             region_code: str = None, relevance_language: str = None, 
             location: str = None, location_radius: str = None,
             channel_id: str = None, channel_type: Literal['show'] = None, event_type: Literal['completed', 'live', 'upcoming'] = None,
             video_caption: Literal['closedCaption', 'none'] = None, video_category_id: str = None,
             video_definition: Literal['high', 'standard'] = None, 
             video_dimension: Literal['2d', '3d'] = None, 
             video_duration: Literal['long', 'medium', 'short'] = None, 
             video_embeddable: Literal['true'] = None, video_license: Literal['creativeCommon', 'youtube'] = None, 
             video_syndicated: Literal['true'] = None, video_type: Literal['episode', 'movie'] = None,
             max_results: int = None, page_token: str = None, on_behalf_of_content_owner: str = None
             ):
        """
        Returns a collection of search results that match the query parameters specified in the API request. 
        """
        
        res = self.client.search().list(
            part='snippet',
            forContentOwner=for_content_owner, forDeveloper=for_developer, forMine=for_mine, relatedToVideoId=related_to_video_id,
            channelId=channel_id, channelType=channel_type, eventType=event_type,
            location=location, locationRadius=location_radius, maxResults=max_results,
            onBehalfOfContentOwner=on_behalf_of_content_owner, order=order, pageToken=page_token,
            publishedAfter=published_atfer, publishedBefore=publised_before, q=q, 
            regionCode=region_code, relevanceLanguage=relevance_language, safeSearch=safe_search,
            topicId=topic_id, type=type,
            videoCaption=video_caption, videoCategoryId=video_category_id, videoDefinition=video_definition,
            videoDimension=video_dimension, videoDuration=video_duration, videoEmbeddable=video_embeddable, 
            videoLicense=video_license, videoSyndicated=video_syndicated, videoType=video_type
        ).execute()
        
        return SearchListResponse._from_response_dict(res)