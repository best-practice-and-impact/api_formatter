import datetime
from custom_variables import DatasetType, AlterType, QualityDesignation, DistributionFormat, MediaType

class datasetConfig:
    
    def __init__(self, id: str, type: DatasetType, title: str, description: str, topics: list[str],
                 next_release: str, keywords: list[str], QMI_href: str, contact_name: str, contact_email: str,
                 contact_telephone: str, publisher_name: str, publisher_href: str):
        self._id: str = id
        self._type: DatasetType = DatasetType(type)
        self._title: str = title
        self._description: str = description
        
        self._topics: list[str] = topics
        self._license: str = "Open Government License v3.0"
        
        self._next_release: str = next_release
        self._keywords: list[str] = keywords
        
        self._QMI: dict = {"href": QMI_href}
        self._Contact: dict = {"name": contact_name, 
                              "email": contact_email,
                              "telephone": contact_telephone}
        self._Publisher: dict = {"name": publisher_name,
                                "href": publisher_href}
        
        def get_id(self):
            return self._id
        
        def set_id(self, new_id):
            self._id = new_id
            
        def get_type(self):
            return self._type
        
        def set_type(self, new_type):
            self._type = new_type
            
        def get_title(self):
            return self._title
        
        def set_title(self, new_title):
            self._title = new_title
            
        def get_description(self):
            return self._description
        
        def set_description(self, new_description):
            self._description = new_description
            
        def get_topics(self):
            return self._topics
        
        def set_topics(self, new_topics):
            self._topics = new_topics
            
        def get_license(self):
            return self._license
        
        def set_license(self, new_license):
            self._license = new_license
            
        
    def __str__(self):
        return f'Dataset: {self.title}, ID: {self.id}'
        
class editionConfig:
    
    def __init__(self, dataset_id: str, edition: str, edition_title: str, release_date: datetime,
                 version: int, last_updated: datetime, quality_designation: QualityDesignation,
                 usage_notes_title: str, usage_notes_note: str, alert_type: AlterType,
                 alert_date: datetime, alert_description: str, distribution_title: str,
                 distribution_format: DistributionFormat, distribution_download_url: str,
                 distribution_byte_size: int, distribution_media_type: MediaType):
        self.dataset_id: str = dataset_id
        self.edition: str = edition
        self.edition_title: str = edition_title
        self.release_date: datetime = release_date
        
        self.version: int = version
        self.last_updated: datetime = last_updated
        self.quality_designation: QualityDesignation = quality_designation
        
        self.Usage_Notes: dict = {"title": usage_notes_title,
                                  "note": usage_notes_note}
        self.Alert: dict = {"type": alert_type,
                            "date": alert_date,
                            "description": alert_description}
        self.Distribution: dict = {"title": distribution_title,
                                   "format": distribution_format,
                                   "download_url": distribution_download_url,
                                   "byte_size": distribution_byte_size,
                                   "media_type": distribution_media_type}
    
    def __str__(self):
        return f'Edition: {self.edition_title}, as part of Dataset: {self.dataset_id}'