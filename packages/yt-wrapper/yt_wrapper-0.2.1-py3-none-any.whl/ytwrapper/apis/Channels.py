from typing import Literal
from ..resources.ChannelResources import ChannelResource, ChannelListResponse
from googleapiclient.discovery import Resource

ChannelPartType = Literal["audit_details",
    "branding_settings", "content_details",
    "content_owner_details",
    "localizations", "snippet",
    "statistics", "status",
    "topic_details"
] | list[
    Literal["audit_details",
        "branding_settings", "content_details",
        "content_owner_details",
        "localizations", "snippet",
        "statistics", "status",
        "topic_details"
    ]
]

ChannelUpdatePartType = Literal['branding_settings', 'status'
                                ]|list[Literal['branding_settings', 'status']]

class Channel:
    def __init__(self, client: Resource) -> None:
        self.client: Resource = client
    
    def list(self, *, part: ChannelPartType,
             for_username: str = None, id: str|list[str] = None, managed_by_me: bool = None, mine: bool = None,
             max_results: int = None, page_token: str = None, 
             on_behalf_of_content_owner: str = None):
        """
        Returns a collection of zero or more `channel` resources that match the request criteria.
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/channels/list)
        """
        
        if len([x for x in (for_username, id, managed_by_me, mine) if x != None]) != 1: 
            raise Exception("No/too many filters specified.")

        if type(part) == list:
            part = ",".join(part)
        if type(id) == list:
            id = ",".join(id)
        
        res = self.client.channels().list(
            part=part,
            forUsername=for_username, id=id, managedByMe=managed_by_me, mine=mine,
            maxResults=max_results, pageToken=page_token,
            onBehalfOfContentOwner=on_behalf_of_content_owner
        ).execute()

        return ChannelListResponse._from_response_dict(res)
    
    def update(self, body: ChannelResource, *, part: ChannelUpdatePartType,
                on_behalf_of_content_owner: str = None):
        """
        Updates a channel's metadata.
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/channels/update)
        """
        request_body = {
            'id': body.id
        }
        
        if 'branding_settings' in part:
            channel = body.branding_settings.channel
            request_body['brandingSettings'] = {'channel': {
                'description': channel.description,
                'country': channel.country,
                'defaultLanguage': channel.default_language,
                'keywords': channel.keywords,
                'moderateComments': channel.moderate_comments,
                'trackingAnalyticsAccountId': channel.tracking_analytics_account_id,
                'unsubscribedTrailer': channel.unsubscribed_trailer,
            }}
        
        if 'status' in part:
            request_body['status'] = {'selfDeclaredMadeForKids': body.status.self_declared_made_for_kids}

        if type(part) == list:
            part = ",".join(part)
            
        res = self.client.channels().update(
            part=part,
            body=request_body,
            onBehalfOfContentOwner=on_behalf_of_content_owner
        ).execute()

        return ChannelResource._from_response_dict(res)