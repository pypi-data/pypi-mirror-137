from typing import Literal
from ..resources.SubscriptionResources import SubscriptionResource, SubscriptionListResponse
from googleapiclient.discovery import Resource

SubscriptionPartType = Literal[
    'content_details', 'snippet', 'subscriber_snippet'\
] | list[Literal[
    'content_details', 'snippet', 'subscriber_snippet'\
]]

class Subscription:
    def __init__(self, client: Resource) -> None:
        self.client: Resource = client

    def list(self, *, part: SubscriptionPartType, 
             channel_id: str = None, id: str|list[str] = None, mine: bool = None, 
             my_subscribers: bool = None, my_recent_subscribers: bool = None,
             for_channel_id: str = None, order: Literal['alphabetical', 'relevance', 'unread'] = None,
             max_results: int = None, page_token: str = None, 
             on_behalf_of_content_owner: str = None, on_behalf_of_content_owner_channel: str = None
             ):
        """
        Returns subscription resources that match the API request criteria.
        For more info, visit\
        [Google's official documentation](https://developers.google.com/youtube/v3/docs/subscriptions/list)
        """
        
        if type(part) == list:
            part = ",".join(part)
        if type(id) == list:
            id = ",".join(id)
        
        res = self.client.subscriptions().list(
            part=part,
            channelId=channel_id, mine=mine, id=id, 
            myRecentSubscribers=my_recent_subscribers, mySubscribers=my_subscribers,
            forChannelId=for_channel_id, order=order, 
            maxResults=max_results, pageToken=page_token,
            onBehalfOfContentOwner=on_behalf_of_content_owner, 
            onBehalfOfContentOwnerChannel=on_behalf_of_content_owner_channel
        ).execute()
        
        return SubscriptionListResponse._from_response_dict(res)

    def insert(self, channel_id: str, *, part: SubscriptionPartType):
        body = {
            'snippet': {
                'resourceId': {
                    'kind': 'youtube#channel',
                    'channelId': channel_id,
                }
            }
        }
        
        if type(part) == list:
            part = ",".join(part)
            
        res = self.client.subscriptions().insert(
            part=part,
            body=body
        ).execute()
        return SubscriptionResource._from_response_dict(res)
    
    def delete(self, subscription_id: str):
        self.client.subscriptions().delete(id=subscription_id).execute()
