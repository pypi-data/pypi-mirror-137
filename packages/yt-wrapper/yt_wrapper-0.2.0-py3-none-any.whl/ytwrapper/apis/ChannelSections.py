from typing import Literal
from ..resources.ChannelSectionResources import ChannelSectionResource, ChannelSectionListResponse
from googleapiclient.discovery import Resource

ChannelSectionPartType = Literal['snippet', 'content_details'
                        ] | list[Literal['snippet', 'content_details']]

class ChannelSection:
    def __init__(self, client: Resource) -> None:
        self.client: Resource = client

    def list(self, *, part: ChannelSectionPartType,
             channel_id: str = None, id: str = None, mine: bool = None,
             on_behalf_of_content_owner: str = None):
        """
        Returns a list of `channelSection` resources that match the API request criteriaeria.
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/channelSections/list)
        """
        
        if type(part) == list:
            part = ",".join(part)
        if type(id) == list:
            id = ",".join(id)
        
        res = self.client.channelSections().list(
            part=part,
            id=id, channelId=channel_id, mine=mine,
            onBehalfOfContentOwner=on_behalf_of_content_owner
        ).execute()
        
        return ChannelSectionListResponse._from_response_dict(res)
    
    def insert(self, body: ChannelSectionResource, *, part: ChannelSectionPartType,
               on_behalf_of_content_owner: str = None, 
               on_behalf_of_content_owner_channel: str = None):
        """
        Adds a channel section to the authenticated user's channel.
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/channelSections/insert)
        """
        request_body = {
            'id': body.id
        }
        
        if 'snippet' in part:
            request_body['snippet'] = {
                'type': body.snippet.type,
                'title': body.snippet.title,
                'position': body.snippet.position,
            }
        if 'content_details' in part:            
            request_body['contentDetails'] = {
                'playlists': body.content_details.playlists,
                'channels': body.content_details.channels,
            }
            
        
        if type(part) == list:
            part = ",".join(part)
        
        res = self.client.channelSections().insert(
            part=part,
            body=request_body,
            onBehalfOfContentOwner=on_behalf_of_content_owner,
            onBehalfOfContentOwnerChannel=on_behalf_of_content_owner_channel,
        ).execute()
        return ChannelSectionResource._from_response_dict(res)
    
    def update(self, body: ChannelSectionResource, *, part: ChannelSectionPartType,
               on_behalf_of_content_owner: str = None):
        """
        Updates a channel section.
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/channelSections/update)
        """
        request_body = {
            'id': body.id
        }
        
        if 'snippet' in part:
            request_body['snippet'] = {
                'type': body.snippet.type,
                'title': body.snippet.title,
                'position': body.snippet.position,
            }
        if 'content_details' in part:            
            request_body['contentDetails'] = {
                'playlists': body.content_details.playlists,
                'channels': body.content_details.channels,
            }
            
        
        if type(part) == list:
            part = ",".join(part)
        
        res = self.client.channelSections().update(
            part=part,
            body=request_body,
            onBehalfOfContentOwner=on_behalf_of_content_owner,
        ).execute()
        return ChannelSectionResource._from_response_dict(res)
    
    def delete(self, section_id: str,
               on_behalf_of_content_owner: str = None):
        """
        Deletes a channel section.
        For more info, visit\
    [Google's official documentation](https://developers.google.com/youtube/v3/docs/channelSections/delete)
        """
        res = self.client.channelSections().delete(
            id=section_id,
            onBehalfOfContentOwner=on_behalf_of_content_owner
        ).execute()
        
