import datetime
from custom_variables import DatasetType, AlertType, QualityDesignation, DistributionFormat, MediaType
import json
import yaml 
from pathlib import Path
import os

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
            "publisher": {"name": "", "href": ""},
            "file": {"path": Path(""), "format": "", "size": 0}
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
        if key == "file": # Coded like this because format and size shouldn't be changed manually
            self._dataset_metadata[key] =  {"path": Path(value),
                                            "format": value.split(".")[-1],
                                            "size": os.path.getsize(value)} # Size in bytes
        elif key in self._dataset_metadata:
            self._dataset_metadata[key] = value
        else:
            raise KeyError(f'{key} is not a config option. Please choose from {list(self._dataset_metadata.keys())}')
        

    #config_path should be raw string not normal string ('\' as separator)
    def load_metadata_from_file(self, config_path: str):
        """Load configuration from a JSON or YAML file and import it into the metadata."""
        #check file extension
        format = config_path.split(".")[-1].lower()
        verified_config_path = Path(config_path)
        
        if not verified_config_path.exists():
            raise FileNotFoundError(f'Configuration file not found: {verified_config_path}')
        
        #load the file content based on format
        try:
            with open(verified_config_path, 'r') as file:
                if format == 'json':
                    loaded_raw_metadata = json.load(file)
                elif format in ['yaml', 'yml']:
                    loaded_raw_metadata = yaml.safe_load(file)
                else:
                    raise ValueError(f'Unsupported file format: {format}. Only "json" and "yaml" are supported.')
        except json.JSONDecodeError as e:
            raise ValueError(f'Error parsing JSON file: {e}')
        except yaml.YAMLError as e:
            raise ValueError(f'Error parsing YAML file: {e}')
    
        # it only validates input dictionary and updates the _dataset_metadata attribute of the instance
        self.import_from_dict(loaded_raw_metadata)

        return loaded_raw_metadata
    
    def export_to_json(self, file_path: str = '/api_formatter/results'):
        """
        Exports the dataset meta data to a json file.

        Parameters
        ----------
        file_path : str, optional
            The directory path for where the json file will be stored, by default '/api_formatter/results'
        """
        with open(f'{file_path}/{self._dataset_metadata.get('title')}_metadata.json', 'w') as fp:
            json.dump(self._dataset_metadata, fp)
        

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
            
            if key == 'distribution':
                try:
                    self._edition_metadata[key]['format'] = DistributionFormat(value['format'])
                except ValueError:
                    print(f'{value['format']} is not valid; possible choices: {list(DistributionFormat)}')
                    return None
            
            self._edition_metadata[key] = value
        
        else:
            raise KeyError(f'{key} is not a config option. Please choose from {list(self._edition_metadata.keys())}')
        

    #config_path should be raw string not normal string ('\' as separator)
    def load_metadata_from_file(self, config_path: str):
        """Load configuration from a JSON or YAML file and import it into the metadata."""
        #check file extension
        format = config_path.split(".")[-1].lower()
        verified_config_path = Path(config_path)
        
        if not verified_config_path.exists():
            raise FileNotFoundError(f'Configuration file not found: {verified_config_path}')
        
        #load the file content based on format
        try:
            with open(verified_config_path, 'r') as file:
                if format == 'json':
                    loaded_raw_metadata = json.load(file)
                elif format in ['yaml', 'yml']:
                    loaded_raw_metadata = yaml.safe_load(file)
                else:
                    raise ValueError(f'Unsupported file format: {format}. Only "json" and "yaml" are supported.')
        except json.JSONDecodeError as e:
            raise ValueError(f'Error parsing JSON file: {e}')
        except yaml.YAMLError as e:
            raise ValueError(f'Error parsing YAML file: {e}')
    
        # it only validates input dictionary and updates the _dataset_metadata attribute of the instance
        self.import_from_dict(loaded_raw_metadata)

        return loaded_raw_metadata
    
    def export_to_json(self, file_path: str = '/api_formatter/results'):
        """
        Exports the edition meta data to a json file.

        Parameters
        ----------
        file_path : str, optional
            The directory path for where the json file will be stored, by default '/api_formatter/results'
        """
        with open(f'{file_path}/{self._edition_metadata.get('edition_title')}_metadata.json', 'w') as fp:
            json.dump(self._edition_metadata, fp)
    
    
    def __str__(self):
        return f'Edition: {self._edition_metadata["edition_title"]}, as part of Dataset: {self._edition_metadata["dataset_id"]}'
    
