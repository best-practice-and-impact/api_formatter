import datetime
import json
from custom_variables import DatasetType, AlertType, QualityDesignation, DistributionFormat, MediaType

class dataset_config:
    
    def __init__(self):
        self._id: str = ""
        self._type: DatasetType = DatasetType()
        self._title: str = ""
        self._description: str = ""
        
        self._topics: list[str] = []
        self._licnese: str = "Open Government License v3.0"
        
        self._next_release: str = ""
        self._keywords: list[str] = []
        
        self._QMI: dict = {"href": ""}
        self._Contact: dict = {"name": "", 
                              "email": "",
                              "telephone": ""}
        self._Publisher: dict = {"name": "",
                                "href": ""}
    
    
    
    def __str__(self):
        return f'Dataset: {self.title}, ID: {self.id}'
        
class edition_config:
    
    def __init__(self):
        self._dataset_id: str = ""
        self._edition: str = ""
        self._edition_title: str = ""
        self._release_data: datetime = ""
        
        self._version: int = 1
        self._last_updated: datetime = ""
        self._quality_designation: QualityDesignation = QualityDesignation()
        
        self._Usage_Notes: dict = {"title": "",
                                  "note": ""}
        self._Alert: dict = {"type": AlertType(),
                            "date": "",
                            "description": ""}
        self._Distribution: dict = {"title": "",
                                   "format": DistributionFormat(),
                                   "download_url": "",
                                   "byte_size": 0,
                                   "media_type": MediaType()}
    
    def import_from_file(self, file):
        with open(file) as f:
            config_file = json.load(f)
        
        self._dataset_id: str = config_file['dataset_id']
        self._edition: str = config_file['edition']
        self._edition_title: str = config_file['edition_title']
        self._release_data: datetime = config_file['release_date']
        #self._version: int = 1
        self._last_updated: datetime = datetime.now()
        self._quality_designation: QualityDesignation = QualityDesignation(config_file['quality_designation'])
        
        self._Usage_Notes: dict = {"title": config_file['Usage_Note']['title'],
                                  "note": config_file['Usage_Note']['note']}
        self._Alert: dict = {"type": AlertType(config_file['Alert']['type']),
                            "date": config_file['Alert']['date'],
                            "description": config_file['Alert']['description']}
        self._Distribution: dict = {"title": config_file['Distribution']['title'],
                                   "format": DistributionFormat(config_file['Distribution']['format']),
                                   "download_url": config_file['Distribution']['download_url'],
                                   "byte_size": 0,
                                   "media_type": MediaType()}
        
        pass
    
    def get_dataset_id(self):
        return self.dataset_id
    
    def __str__(self):
        return f'Edition: {self.edition_title}, as part of Dataset: {self.dataset_id}'