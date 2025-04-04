import datetime
from custom_variables import DatasetType, AlertType, QualityDesignation, DistributionFormat, MediaType

class datasetConfig:
    
    def __init__(self):

        self._dataset_metadata = {"id": "",
                                  "type": "",
                                  "title": "",
                                  "description": "",
                                  "topics": [],
                                  "license": "Open Government License v3.0",
                                  "next_release": "",
                                  "keywords": [],
                                  "QMI": {"href": ""},
                                  "contact": {"name": "", "email": "", "telephone": ""},
                                  "publisher": {"name": "", "href": ""}}
            
    def import_from_dict(self, new_meta_data: dict):
        if list(self._dataset_metadata.keys()) == list(new_meta_data.keys()):
            self._dataset_metadata = new_meta_data
        else:
            raise KeyError(f'ERROR: The config fields in the dictonary you are trying to use are incorrect.\nPlease make sure you are using these fields for your config file:{list(self._dataset_metadata.keys())}')
    
    def get(self, key: str):
        return self._dataset_metadata.get(key)
    
    def set(self, key: str, value: str):
        if key == "type":
            try:
                value = DatasetType(value)
            except ValueError:
                print(f'{value} is not valid; possible choices: {list(QualityDesignation)}')
                return None
        if key in self._dataset_metadata:
            self._dataset_metadata[key] = value
        else:
            raise KeyError(f'{key} is not a config option. Please choose from {list(self._dataset_metadata.keys())}')
        
        
    def __str__(self):
        return f'Dataset: {self._dataset_metadata["title"]}, ID: {self._dataset_metadata["id"]}'
        
class editionConfig:
    
    def __init__(self, dataset_id: str, edition: str, edition_title: str, release_date: datetime,
                 version: int, last_updated: datetime, quality_designation: QualityDesignation,
                 usage_notes_title: str, usage_notes_note: str, alert_type: AlertType,
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
    
    def get_dataset_id(self) -> str:
        return self.dataset_id
    
    def set_dataset_id(self, new_id: str):
        self.dataset_id = new_id
        
    def get_edition(self) -> str:
        return self.edition
    
    def set_edition(self, new_edition: str):
        self.edition = new_edition
        
    def get_edition_title(self) -> str:
        return self.edition_title
    
    def set_edition_title(self, new_title: str):
        self.edition_title = new_title
        
    def get_release_date(self) -> datetime:
        return self.release_date
    
    def set_release_date(self, new_release_date: str):
        self.release_date = datetime.strptime(new_release_date, '%d\%m\%Y')
        
    def get_version(self) -> int:
        return self.version
        
    def get_last_updated(self) -> datetime:
        return self.last_updated
    
    def get_quality_designation(self) -> QualityDesignation:
        return self.quality_designation
    
    def set_quality_designation(self, new_designation: str):
        try:
            self.quality_designation = QualityDesignation(new_designation)
        except ValueError:
            # more informative error message
            raise ValueError(f'{new_designation} is not valid; possible choices: {list(QualityDesignation)}')
        
    def get_usage_notes_full(self) -> dict:
        return self.Usage_Notes
    
    def set_usage_notes_full(self, new_usage_notes: dict):
        self.Usage_Notes = new_usage_notes
        
    def get_usage_notes_title(self) -> str:
        return self.Usage_Notes['title']
    
    def set_usage_notes_title(self, new_title: str):
        self.Usage_Notes['title'] = new_title
        
    def get_usage_notes_note(self) -> str:
        return self.Usage_Notes['note']
    
    def set_usage_notes_note(self, new_note: str):
        self.Usage_Notes['note'] = new_note
    
    def get_alert_full(self) -> dict:
        return self.Alert
    
    def set_alert_full(self, new_alert: dict):
        self.Alert = new_alert
        
    def get_alert_type(self) -> AlertType:
        return self.Alert['type']
    
    def set_alert_type(self, new_type: str):
        try:
            self.Alert['type'] = AlertType(new_type)
        except ValueError:
            # more informative error message
            raise ValueError(f'{new_type} is not valid; possible choices: {list(AlertType)}')
        
    def get_alert_date(self) -> datetime:
        return self.Alert['date']
    
    def set_alert_date(self, new_date: str):
        self.Alert['date'] = datetime.strptime(new_date, '%d\%m\%Y')
        
    def get_alert_description(self) -> str:
        return self.Alert['description']
    
    def set_alert_description(self, new_description: str):
        self.Alert['description'] = new_description
        
    def get_distribution_full(self) -> dict:
        return self.Distribution
    
    def set_distribution_full(self, new_distribution: dict):
        self.Distribution = new_distribution
        
    def get_distribution_title(self) -> str:
        return self.Distribution['title']
    
    def set_distribution_title(self, new_title: str):
        self.Distribution['title'] = new_title
        
    def get_distribution_format(self) -> DistributionFormat:
        return self.Distribution['format']
    
    def set_distribution_format(self, new_format: DistributionFormat):
        try:
            self.Distribution['format'] = DistributionFormat(new_format)
        except ValueError:
            # more informative error message
            raise ValueError(f'{new_format} is not valid; possible choices: {list(DistributionFormat)}')

    def get_distribution_download_url(self) -> str:
        return self.Distribution['download_url']
        
    def set_distribution_download_url(self, new_url: str):
        self.Distribution['download_url'] = new_url
    
    def get_distribution_byte_size(self) -> int:
        return self.Distribution['byte_size']
    
    def get_distribution_media_type(self) -> MediaType:
        return self.Distribution['media_type']
    
    def __str__(self):
        return f'Edition: {self.edition_title}, as part of Dataset: {self.dataset_id}'