from ..resources.I18nResources import I18nLanguageListResponse, I18nRegionListResponse
from googleapiclient.discovery import Resource

class I18n:
    def __init__(self, client: Resource) -> None:
        self.client = client
        
    def list_languages(self):
        req = self.client.i18nLanguages().list(part='snippet')
        return I18nLanguageListResponse._from_response_dict(req.execute())
    
    def list_regions(self):
        req = self.client.i18nRegions().list(part='snippet')
        return I18nRegionListResponse._from_response_dict(req.execute())
        ...
