from typing import Literal
from ..resources.CommentThreadResources import CommentThreadResource, CommentThreadListResponse
from googleapiclient.discovery import Resource

CommentThreadPartType = Literal["snippet", "replies"] | list[
        Literal["snippet", "replies"]
    ]

class CommentThread:
    def __init__(self, client: Resource) -> None:
        self.client: Resource = client
        
    def list(self, *, part: CommentThreadPartType, 
             id: str = None, channel_id: str = None, video_id: str = None,
             all_threads_related_to_channel_id: str = None, 
             max_results: int = 20, 
             moderation_status: Literal['held_for_review', 'likely_spam', 'published'] = None,
             order: Literal['time', 'relevance'] = None, 
             text_format: Literal['html', 'plain_text'] = None,
             page_token: str = None, search_terms: str = None):
        """
        Returns a list of comment threads that match the API request parameters.
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/playlists/list)
        """
        
        if type(part) == list:
            part = ",".join(part)
        if type(id) == list:
            id = ",".join(id)
            
        if text_format == "plain_text":
            text_format = "plainText"
        if moderation_status == "held_for_review":
            moderation_status = "heldForReview"
        elif moderation_status == "likely_spam":
            moderation_status = "likelySpam"
            
        req = self.client.commentThreads().list(
            part=part,
            id=id, channelId=channel_id, videoId=video_id,
            allThreadsRelatedToChannelId=all_threads_related_to_channel_id,
            maxResults=max_results, moderationStatus=moderation_status,
            order=order, pageToken=page_token, searchTerms=search_terms, textFormat=text_format
        )
        res = req.execute()
        
        return CommentThreadListResponse._from_response_dict(res)
    
    def insert(self, body: CommentThreadResource, *, part: CommentThreadPartType = "snippet"):
        """
        Creates a new top-level comment.
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/playlists/list)
        """
        request_body = {
            'snippet': {
                'videoId': body.snippet.video_id,
                'channelId': body.snippet.channel_id,
                'topLevelComment': {
                    'snippet': {
                        'textOriginal': body.snippet.top_level_comment.snippet.text_original
                    }
                }
            }
        }
        if type(part) == list:
            part = ",".join(part)
            
        req = self.client.commentThreads().insert(
            body=request_body,
            part=part
        )
        
        return CommentThreadResource._from_response_dict(req.execute())