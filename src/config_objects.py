import datetime
from custom_variables import DatasetType, AlertType, QualityDesignation, DistributionFormat, MediaType
import json
import yaml 
from pathlib import Path
import os

class datasetConfig:
    """
    A class to store metadata about a dataset.
    
    Attributes
    ----------
    dataset_metadata : dict
        Metadata properties as keys and their values. Properties include
        title, description, and license, among others.
        
    Methods
    -------
    import_from_dict(new_meta_data):
        Imports metadata from a pre-existing dictionary.
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
            
    def import_from_dict(self, new_metadata: dict):
        """
        Imports metadata from a pre-existing dictionary. Will not
        overwrite or empty any values in the existing dictionary
        that are not specified in new_metadata.

        Parameters
        ----------
        new_metadata : dict
            External dictionary to be imported

        Raises
        ------
        KeyError:
            If a key in the supplied dictionary isn't contained within
            the existing class metadata dictionary
        """
        for key, value in new_metadata.items():
            if key in self._dataset_metadata.keys():
                self.set(key, value)
            else:
                raise KeyError(f'ERROR: The config fields in the dictonary you\
                               are trying to use are incorrect.\nPlease make\
                               sure you are using only these fields for your\
                               config file:{list(self._dataset_metadata.keys())}')

    def get(self, key: str):
        """
        Get the value associated with a key in the metadata dictionary.

        Parameters
        ----------
        key : str
            Key used to index metadata

        Returns
        -------
        obj
            Value associated with key
        
        Raises
        ------
        KeyError 
            If the supplied key is not a key in the metadata dictionary
        """
        if key in self._dataset_metadata:
            return self._dataset_metadata.get(key)
        else:
            raise KeyError(f'{key} is not a config option. Please choose\
                           from {list(self._dataset_metadata.keys())}')

    def set(self, key: str, value: str):
        """
        Sets the value of a key within the metadata dictionary
        to a new value.

        Parameters
        ----------
        key : str
            Key used to index metadata
        value : str
            New metadata value for the corresponding key

        Returns
        -------
        None
            If the value for "type" isn't an allowed option.

        Raises
        ------
        KeyError
            If the supplied key is not a key in the metadata dictionary
        """
        if key == "type":
            try:
                value = DatasetType(value)
            except ValueError:
                print(f'{value} is not valid; possible choices: {list(DatasetType)}')
                return None
        if key == "file": # Coded like this because format and size shouldn't be changed manually
            self._dataset_metadata[key] =  {"path": Path(value),
                                            "format": value.split(".")[-1],
                                            "size": os.path.getsize(value)} # Size in bytes
        elif key in self._dataset_metadata:
            self._dataset_metadata[key] = value
        else:
            raise KeyError(f'{key} is not a config option. Please choose from {list(self._dataset_metadata.keys())}')

    def load_metadata_from_file(self, config_path: str):
        """
        Load configuration from a JSON or YAML file and import it into the metadata.
        
        Parameters
        ----------
        config_path : str (raw)
            Path to the file to load into the metadata dictionary. Should
            be supplied as a raw string (r'string') with backslash as a
            path seperator
        
        Returns
        -------
        obj
            The loaded raw metadata
        
        Raises
        ------
        FileNotFoundError
            If the file at config_path cannot be found.
        ValueError
            If the file at config_path is not .yaml or .json, or if
            there is an error parsing a .yaml or .json.
        """
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
        Exports the dataset metadata to a .json file.

        Parameters
        ----------
        file_path : str, optional
            The directory path for where the .json file will be stored, by default '/api_formatter/results'
        """
        with open(f'{file_path}/{self._dataset_metadata.get('title')}_metadata.json', 'w') as fp:
            json.dump(self._dataset_metadata, fp)
    
    def __str__(self):
        return f'Dataset: {self._dataset_metadata["title"]}, ID: {self._dataset_metadata["id"]}'
        
class editionConfig:
    """
    A class that stores metadata about individual editions of datasets.
    
    Attributes
    ----------
    edition_metadata : dict
        Metadata properties as keys and their values. Properties
        include version, release_date, and quality_designation, among others.
        
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
        Constructs the initial dictionary for storing metadata.
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
    
    def import_from_dict(self, new_metadata: dict):
        """
        Imports metadata from a pre-existing dictionary. Will not
        overwrite or empty any values in the existing dictionary
        that are not specified in new_metadata.

        Parameters
        ----------
        new_metadata : dict
            External dictionary to be imported
        
        Raises
        ------
        KeyError:
            If a key in new_metadata isn't in the Class metadata dictionary
        """
        for key, value in new_metadata.items():
            if key in self._edition_metadata.keys():
                self.set(key, value)
            else:
                raise KeyError(f'One or more fields in the config dictionary \
                               is invalid.\n Please use only allowed \
                               fields as keys:{list(self._dataset_metadata.keys())}')

    def get(self, key: str):
        """
        Get the value associated with a key in the metadata dictionary.

        Parameters
        ----------
        key : str
            Key used to index metadata

        Returns
        -------
        obj
            Value associate with supplied key
        
        Raises
        ------
        KeyError
            If the supplied key is not a field in the metadata
        """
        if key in self._edition_metadata:
            return self._edition_metadata.get(key)
        else:
            raise KeyError(f'{key} is not a present in the metadata. \
                           Please choose from {list(self._edition_metadata.keys())}')
    
    def set(self, key: str, value: str):
        """
        Update the value of a given key in the metadata dictionary.

        Parameters
        ----------
        key : str
            Key used to index metadata
        value : str
            New metadata value for the supplied key

        Returns
        -------
        None
            If the value entered for "quality_designation", "alert", or "distribution" 
            isn't an allowed option, or if the value for "release_date" is in the wrong format

        Raises
        ------
        KeyError
            Raised if the key is not a field in the metadata dictionary
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
                    print('There is an error with the supplied alert value.')
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
        """Load configuration from a JSON or YAML file and import it into the metadata.
        
        Parameters
        ----------
        config_path : str (raw)
            Path to the file to load into the metadata dictionary. Should
            be supplied as a raw string (r'string') with backslash as a
            path seperator
        
        Returns
        -------
        obj
            Loaded .json or .yaml file.

        Raises
        ------
        FileNotFoundError
            If the file cannot be found at config_path
        ValueError
            If the file at config_path is not a .json or .yaml, or if
            there is an error parsing the .json or .yaml at config_path.
        """
        format = config_path.split(".")[-1].lower()
        verified_config_path = Path(config_path)
        
        if not verified_config_path.exists():
            raise FileNotFoundError(f'Configuration file not found: {verified_config_path}')
        
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
        Exports the edition metadata to a .json file.

        Parameters
        ----------
        file_path : str, optional
            The directory path for where the json file will be stored, by default '/api_formatter/results'
        """
        with open(f'{file_path}/{self._edition_metadata.get('edition_title')}_metadata.json', 'w') as fp:
            json.dump(self._edition_metadata, fp)
    
    def __str__(self):
        return f'Edition: {self._edition_metadata["edition_title"]}, as part of Dataset: {self._edition_metadata["dataset_id"]}'
    
