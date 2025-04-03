import datetime
from custom_variables import DatasetType, AlertType, QualityDesignation, DistributionFormat, MediaType

class datasetConfig:
    
    def __init__(self, id: str = "", type: DatasetType = "", title: str = "", description: str = "", topics: list[str] = [],
                 next_release: str = "", keywords: list[str] = [], QMI_href: str = "", contact_name: str = "", contact_email: str = "",
                 contact_telephone: str = "", publisher_name: str = "", publisher_href: str = ""):
        self._id: str = id
        self._type: DatasetType = DatasetType(type)
        self._title: str = title
        self._description: str = description
        
        self._topics: list[str] = topics
        self._license: str = "Open Government License v3.0"
        
        self._next_release: str = next_release # This field is designated a string on the plan but both date related fields in edition are datetime objects. I believe this should also be a datetime object, both for the sake of consistancy and to make error checking easier.
        self._keywords: list[str] = keywords
        
        self._QMI: dict = {"href": QMI_href}
        self._Contact: dict = {"name": contact_name, 
                              "email": contact_email,
                              "telephone": contact_telephone}
        self._Publisher: dict = {"name": publisher_name,
                                "href": publisher_href}
        
        def get_id(self) -> str:
            return self._id
        
        def set_id(self, new_id: str):
            self._id = new_id
            
        def get_type(self) -> DatasetType:
            return self._type
        
        def set_type(self, new_type: str): 
            try:
                self._type = DatasetType(new_type)
            except ValueError:
                # more informative error message
                raise ValueError(f'{new_type} is not valid; possible choices: {list(DatasetType)}')
            
        def get_title(self) -> str:
            return self._title
        
        def set_title(self, new_title: str):
            self._title = new_title
            
        def get_description(self) -> str:
            return self._description
        
        def set_description(self, new_description: str):
            self._description = new_description
            
        def get_topics(self) -> list[str]:
            return self._topics
        
        def set_topics(self, new_topics: list[str]):
            self._topics = new_topics
            
        def get_license(self) -> str:
            return self._license
          
        # The set method is here for now, as it was mentioned in the plan that an option for changing the license should be later allowed.    
        def set_license(self, new_license: str):
            self._license = new_license
            
        def get_next_release(self) -> str:
            return self._next_release
        
        def set_next_release(self, new_next_release: str):
            self._next_release = new_next_release
            
        def get_keywords(self) -> list[str]:
            return self._keywords
        
        def set_keywords(self, new_keywords: list[str]):
            self._keywords = new_keywords
            
        def get_QMI_full(self) -> dict:
            return self._QMI
        
        def set_QMI_full(self, new_QMI: dict):
            self._QMI = new_QMI
            
        def get_contact_full(self) -> dict:
            return self._Contact
        
        def set_contact_full(self, new_contact: dict):
            self._Contact = new_contact
            
        def get_contact_name(self) -> str:
            return self._Contact['name']
        
        def set_contact_name(self, new_name: str):
            self._Contact['name'] = new_name
            
        def get_contact_email(self) -> str:
            return self._Contact['email']
        
        def set_contact_email(self, new_email: str):
            self._Contact['email'] = new_email
            
        def get_contact_telephone(self) -> str:
            return self._Contact['telephone']
        
        def set_contact_telephone(self, new_telephone: str):
            self._Contact['telephone'] = new_telephone
            
        def get_publisher_full(self) -> dict:
            return self._Publisher
        
        def set_publisher_full(self, new_publisher: dict):
            self._Publisher = new_publisher
            
        def get_publisher_name(self) -> str:
            return self._Publisher['name']
        
        def set_publisher_name(self, new_name: str):
            self._Publisher['name'] = new_name
        
        def get_publisher_href(self) -> str:
            return self._Publisher['href']
        
        def set_publisher_href(self, new_href: str):
            self._Publisher['href'] = new_href
            
        
    def __str__(self):
        return f'Dataset: {self.title}, ID: {self.id}'
        
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