import os
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.discovery import Resource
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from .apis import Playlist, PlaylistItem, Video, Thumbnail, Comment, CommentThread, \
I18n, VideoCategory, VideoAbuseReportReason, Channel, ChannelSection, Search, Subscription

class Client:
    def __init__(self) -> None:
        self.client: Resource = ...
        
    def _init_resources(self):
        """Adds resources to the class."""
        self.playlist = Playlist(self.client)
        self.playlist_item = PlaylistItem(self.client)
        self.video = Video(self.client)
        self.thumbnail = Thumbnail(self.client)
        self.comment = Comment(self.client)
        self.comment_thread = CommentThread(self.client)
        self.i18n = I18n(self.client)
        self.video_category = VideoCategory(self.client)
        self.video_abuse_report_reason = VideoAbuseReportReason(self.client)
        self.channel = Channel(self.client)
        self.channel_section = ChannelSection(self.client)
        self.search = Search(self.client)
        self.subscription = Subscription(self.client)
        
    def _save_creds(self, creds: Credentials, token_store: str):
        """Saves credentials to a token cache."""
        with open(token_store, 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(creds, f)
        
    def _fetch_new_creds(self, client_secrets_file: str, scopes: list[str]):
        """Fetches new credentials."""
        
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
        credentials = flow.run_console()
        
        return credentials
    
    @classmethod
    def from_client_secrets(cls, client_secrets_file: str, scopes: list[str], 
                            token_store: str = "token.pickle"):
        """
        Returns a youtube client.
        
        Parameters:
            `client_secrets_file`: the path to your client secrets file. 
            `scopes`: the scopes of this client.
            `token_store`: the file the program will use to store credentials for later use.
            
        Returns:
            An instance of the Youtube client, with OAuth2 access.
        """
        
        inst = cls()
        
        credentials: Credentials = None
        
        # * gets stored creds
        if os.path.exists(token_store):
            print("Loading credentials from file...")
            with open(token_store, 'rb') as token:
                credentials = pickle.load(token)
        
        # * Refreshes the access token/fetches new creds
        # * Saves it in token.pickle at the end
        if not credentials or not credentials.valid:
            try:
                print('Refreshing acess token...')
                request = Request()
                credentials.refresh(request)
                print("Access token refreshed!")
            except:
                print("Fetching new credentials...")
                credentials = inst._fetch_new_creds(client_secrets_file, scopes)
                print("New credentails fetched!")
            finally:
                inst._save_creds(credentials, token_store)
        
        youtube = googleapiclient.discovery.build(
            "youtube", "v3", credentials=credentials)
        
        inst.client = youtube
        inst._init_resources()
        return inst
