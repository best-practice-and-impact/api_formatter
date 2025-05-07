import datetime
from custom_variables import DatasetType, AlertType, QualityDesignation, DistributionFormat, MediaType

class datasetConfig:
    """
    A class used to store meta data about a dataset.
    
    ...
    
    Attributes
    ----------
    dataset_metadata : dict
        A dictionary containing all the different fields of the meta data
        
    Methods
    -------
    import_from_dict(new_meta_data):
        Imports meta data from a pre-existing dictionary.
    get(key):
        Get the value of the corresponding key within the meta data.
    set(key, value):
        Sets the value of the corresponding key within the meta data to a new value.
    """
    def __init__(self):
        """
        Constructs the initial dictionary for storing meta data.
        """
        self._dataset_metadata = {
            "id": "",
            "type": DatasetType(),
            "title": "",
            "description": "",
            "topics": [],
            "license": "Open Government License v3.0",
            "next_release": "",
            "keywords": [],
            "QMI": {"href": ""},
            "contact": {"name": "", "email": "", "telephone": ""},
            "publisher": {"name": "", "href": ""}
        }
            
    def import_from_dict(self, new_meta_data: dict):
        """
        Imports meta data from a pre-existing dictionary.

        Parameters
        ----------
        new_meta_data : dict
            External dictionary to be imported
        
        Raises
        ------
        KeyError: Raised if a one of keys in the external dictionary isn't part of the meta data dictionary
        """
        
        for key, value in new_meta_data.items():
            if key in self._dataset_metadata.keys():
                self.set(key, value)
            else:
                raise KeyError(f'ERROR: The config fields in the dictonary you are trying to use are incorrect.\nPlease make sure you are using these fields for your config file:{list(self._dataset_metadata.keys())}')

                    
        
    def get(self, key: str):
        """
        Get the value of the corresponding key within the meta data.

        Parameters
        ----------
        key : str
            Key used to index meta data

        Returns
        -------
        obj
            Value of inputed key
        
        Raises
        ------
        KeyError 
            Raised if the key inputed is not a field in the meta data
        """
        if key in self._dataset_metadata:
            return self._dataset_metadata.get(key)
        else:
            raise KeyError(f'{key} is not a config option. Please choose from {list(self._dataset_metadata.keys())}')
    
    def set(self, key: str, value: str):
        """
        Sets the value of the corresponding key within the meta data to a new value.

        Parameters
        ----------
        key : str
            Key used to index meta data
        value : str
            New meta data vlaue for the corresponding key

        Returns
        -------
        None
            Ends function if the value entered for "type" isn't one of its options

        Raises
        ------
        KeyError
            Raised if the key inputed is not a field in the meta data
        """
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
    """
    A class that stores meta data about individual editions
    
    ...
    
    Attributes
    ----------
    edition_metadata : dict
        A dictionary containing all the different fields of the meta data
        
    Methods
    -------
    import_from_dict(new_meta_data):
        Imports meta data from a pre-existing dictionary.
    get(key):
        Get the value of the corresponding key within the meta data.
    set(key, value):
        Sets the value of the corresponding key within the meta data to a new value.
    """
    def __init__(self):
        """
        Constructs the initial dictionary for storing meta data.
        """
        self._edition_metadata = {
            "dataset_id": "",
            "edition": "",
            "edition_title": "",
            "release_date": datetime(2050, 1, 1),
            "version": 0,
            "last_updated": datetime.now(),
            "quality_designation": QualityDesignation(),
            "usage_notes": {"title": "", "note": ""},
            "alert": {"type": AlertType(), "date": datetime(2050, 1, 1), "description": ""},
            "distribution": {"title": "", "format": DistributionFormat(), "download_url": "", "byte_size": 0, "media_type": MediaType()}
        }
    
    def import_from_dict(self, new_meta_data: dict):
        """
        Imports meta data from a pre-existing dictionary.

        Parameters
        ----------
        new_meta_data : dict
            External dictionary to be imported
        
        Raises
        ------
        KeyError: Raised if a one of keys in the external dictionary isn't part of the meta data dictionary
        """
        
        for key, value in new_meta_data.items():
            if key in self._edition_metadata.keys():
                self.set(key, value)
            else:
                raise KeyError(f'ERROR: The config fields in the dictonary you are trying to use are incorrect.\nPlease make sure you are using these fields for your config file:{list(self._dataset_metadata.keys())}')

    def get(self, key: str):
        """
        Get the value of the corresponding key within the meta data.

        Parameters
        ----------
        key : str
            Key used to index meta data

        Returns
        -------
        obj
            Value of inputed key
        
        Raises
        ------
        KeyError 
            Raised if the key inputed is not a field in the meta data
        """ 
        if key in self._edition_metadata:
            return self._edition_metadata.get(key)
        else:
            raise KeyError(f'{key} is not a config option. Please choose from {list(self._edition_metadata.keys())}')
    
    def set(self, key: str, value: str):
        """
        Sets the value of the corresponding key within the meta data to a new value.

        Parameters
        ----------
        key : str
            Key used to index meta data
        value : str
            New meta data vlaue for the corresponding key

        Returns
        -------
        None
            Ends function if the value entered for "quality_designation", "alert" or "distribuation" 
            isn't one of its options or when the value for "release_date" is in the wrong format

        Raises
        ------
        KeyError
            Raised if the key inputed is not a field in the meta data
        """
        
        if key == "quality_designation":
            try:
                value = QualityDesignation(value)
            except ValueError:
                print(f'{value} is not valid; possible choices: {list(QualityDesignation)}')
                return None
            
        if key == "release_date":
            try:
                value = datetime.strptime(value, "%d/%m/%Y")
            except ValueError:
                print(f'{value} is the wrong datetime format. Try "dd/mm/yyyy".')
                return None
            
        if key in self._edition_metadata:
            
            if key == 'alert':
                try:
                    self._edition_metadata[key]['type'] = AlertType(value['type'])
                    self._edition_metadata[key]['date'] = datetime.strptime(value['date'], '%d/%m/%Y')
                except ValueError:
                    print('There is an error with you alert values.')
                    return None
            
            if key == 'distribuation':
                try:
                    self._edition_metadata[key]['format'] = DistributionFormat(value['format'])
                except ValueError:
                    print(f'{value['format']} is not valid; possible choices: {list(DistributionFormat)}')
                    return None
            
            self._edition_metadata[key] = value
        
        else:
            raise KeyError(f'{key} is not a config option. Please choose from {list(self._dataset_metadata.keys())}')
    
    
    def __str__(self):
        return f'Edition: {self._edition_metadata["edition_title"]}, as part of Dataset: {self._edition_metadata["dataset_id"]}'