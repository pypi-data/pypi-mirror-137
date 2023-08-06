from typing import Literal
from ..resources.CommentResources import CommentListResponse, CommentResource
from googleapiclient.discovery import Resource

CommentPartType = Literal["snippet"]|list[Literal["snippet"]]

class Comment:
    def __init__(self, client: Resource) -> None:
        self.client: Resource = client
    
    def list(self, *, part: CommentPartType = "snippet", 
             id: list[str] | str = None, parent_id: str = None,
             max_results: int = None, page_token: str = None, 
             text_format: Literal['html', 'plain_text'] = None):
        """
        Returns a list of comments that match the API request parameters.
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/comments/list)
        """
        
        if type(part) == list:
            part = ",".join(part)
        if type(id) == list:
            id = ",".join(id)
        if text_format == "plain_text":
            text_format = "plainText"
            
        req = self.client.comments().list(part=part, id=id, parentId=parent_id,
                                          maxResults=max_results, pageToken=page_token,
                                          textFormat=text_format)
        return CommentListResponse._from_response_dict(req.execute())
    
    def insert(self, body: CommentResource, *, part: CommentPartType = "snippet"):
        """
        Creates a reply to an existing comment. 
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/comments/insert)
        """
        if type(part) == list:
            part = ",".join(part)
        
        request_body = {
            'snippet': {
                'textOriginal': body.snippet.text_original,
                'parentId': body.snippet.parent_id,
            }
        }
        
        req = self.client.comments().insert(
            part=part,
            body=request_body
        )
        return CommentResource._from_response_dict(req.execute())
    
    def update(self, body: CommentResource, *, part: CommentPartType = "snippet"):
        """
        Modifies a comment.
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/comments/update)
        """
        if type(part) == list:
            part = ",".join(part)
        
        request_body = {
            'snippet': {
                'textOriginal': body.snippet.text_original,
            },
            'id': body.id
        }
        
        req = self.client.comments().update(
            part=part,
            body=request_body
        )
        return CommentResource._from_response_dict(req.execute())
    
    def delete(self, comment_id: str):
        """
        Deletes a comment.
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/comments/delete)
        """
        self.client.comments().delete(id=comment_id).execute()