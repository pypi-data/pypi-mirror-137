from typing import Literal
from ..resources.PlaylistResources import PlaylistListResponse, PlaylistResource
from googleapiclient.discovery import Resource

PlaylistPartType = Literal["content_details", "localizations", 
            "player", "snippet", "status"] | list[
                Literal["content_details", "localizations", 
                        "player", "snippet", "status"]]

class Playlist:
    def __init__(self, client: Resource) -> None:
        self.client = client
    
    def list(self, *, part: PlaylistPartType,
             channel_id : str = None, id: list[str] | str = None, mine: bool = None,
             max_results: int = 5, page_token: str = "",
             on_behalf_of_content_owner: str = None
             ):
        """
        Returns a collection of playlists that match the API request parameters.
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/playlists/list)
        """
        if len([x for x in (channel_id, id, mine) if x != None]) != 1: 
            raise Exception("No/too many filters specified.")
        
        if type(part) == list:
            part = ",".join(part)
        if type(id) == list:
            id = ",".join(id)
        
        response = self.client.playlists().list(part=part,
                                     channelId=channel_id,
                                     id=id,
                                     mine=mine,
                                     maxResults=max_results,
                                     pageToken=page_token,
                                     onBehalfOfContentOwner=on_behalf_of_content_owner).execute()
        return PlaylistListResponse._from_response_dict(response)
    
    def insert(self, body: PlaylistResource, *, part: PlaylistPartType,
               on_behalf_of_content_owner: str = None):
        """
        Creates a playlist.
        For more info, visit\
    [Google's official documentation](https://developers.google.com/youtube/v3/docs/playlists/insert)
        """
        if not body.snippet.title: raise Exception("Playlist title not provided")
        
        if type(part) == list:
            part = ",".join(part)
            
        request_body = {
            "snippet": {
                "title": body.snippet.title,
                "description": body.snippet.description
            }
        }
        if "status" in part:
            request_body["status"] = {"privacyStatus": body.status.privacy_status}
            
        req = self.client.playlists().insert(body=request_body, part=part,
                                             onBehalfOfContentOwner=on_behalf_of_content_owner)
        res = PlaylistResource._from_response_dict(req.execute())
        return res
        
    
    def update(self, body: PlaylistResource, *, part: PlaylistPartType,
               on_behalf_of_content_owner: str = None):
        """
        Modifies a playlist.\
        For example, you could change a playlist's title, description, or privacy status. 
        For more info, visit\
    [Google's official documentation](https://developers.google.com/youtube/v3/docs/playlists/update)
        """
        if not body.snippet.title or "snippet" not in part: 
            raise Exception("Playlist title not provided")
        if not body.id: raise Exception("Playlist id not provided")

        if type(part) == list:
            part = ",".join(part)
        
        request_body = {
            "id": body.id,
            "snippet": {
                "title": body.snippet.title,
                "description": body.snippet.description,
            }
        }
        
        if "status" in part:
            request_body["status"] = {"privacyStatus": body.status.privacy_status}
            
        req = self.client.playlists().update(body=request_body, part=part,
                                             onBehalfOfContentOwner=on_behalf_of_content_owner)
        res = PlaylistResource._from_response_dict(req.execute())
        return res
    
    def delete(self, playlist_id: str,
               on_behalf_of_content_owner: str = None):
        """
        Deletes a playlist.
        For more info, visit\
    [Google's official documentation](https://developers.google.com/youtube/v3/docs/playlists/delete)
        """
        request = self.client.playlists().delete(
            id=playlist_id,
            onBehalfOfContentOwner=on_behalf_of_content_owner
        )
        request.execute()