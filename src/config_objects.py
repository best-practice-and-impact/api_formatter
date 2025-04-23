import datetime
from custom_variables import DatasetType, AlertType, QualityDesignation, DistributionFormat, MediaType
import json
import yaml 
from pathlib import Path

class datasetConfig:
    
    def __init__(self):

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
        if list(self._dataset_metadata.keys()) == list(new_meta_data.keys()):
            self._dataset_metadata = new_meta_data
            self.set("type", new_meta_data["type"])
        else:
            raise KeyError(f'ERROR: The config fields in the dictonary you are trying to use are incorrect.\nPlease make sure you are using these fields for your config file:{list(self._dataset_metadata.keys())}')
    
    def get(self, key: str):
        if key in self._dataset_metadata:
            return self._dataset_metadata.get(key)
        else:
            raise KeyError(f'{key} is not a config option. Please choose from {list(self._dataset_metadata.keys())}')
    
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
        

    #config_path should be raw string not normal string ('\' as separator)
    def load_metadata_from_file(self, config_path: str):
        """Load configuration from a JSON or YAML file and import it into the metadata."""
        #check file extension
        format = config_path.split(".")[-1].lower()
        verified_config_path = Path(config_path)
        
        if not verified_config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {verified_config_path}")
        
        #load the file content based on format
        try:
            with open(verified_config_path, 'r') as file:
                if format == 'json':
                    loaded_raw_metadata = json.load(file)
                elif format in ['yaml', 'yml']:
                    loaded_raw_metadata = yaml.safe_load(file)
                else:
                    raise ValueError(f"Unsupported file format: {format}. Only 'json' and 'yaml' are supported.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON file: {e}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")
    
        # it only validates input dictionary and updates the _dataset_metadata attribute of the instance
        self.import_from_dict(loaded_raw_metadata)

        return loaded_raw_metadata

        
        
    def __str__(self):
        return f'Dataset: {self._dataset_metadata["title"]}, ID: {self._dataset_metadata["id"]}'
        
class editionConfig:
    
    def __init__(self):
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
        
    def get(self, key: str):
        if key in self._edition_metadata:
            return self._edition_metadata.get(key)
        else:
            raise KeyError(f'{key} is not a config option. Please choose from {list(self._edition_metadata.keys())}')
    
    def set(self, key: str, value: str):
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
        
        if key in self._edition_metadata:
            self._edition_metadata[key] = value
            
            if key == 'alert':
                try:
                    self._edition_metadata[key]['type'] = AlertType(value['type'])
                    self._edition_metadata[key]['date'] = datetime.strptime(value['date'], '%d/%m/%Y')
                except ValueError:
                    print('There is an error with you alert values.')
            
            if key == 'distribuation':
                try:
                    self._edition_metadata[key]['format'] = DistributionFormat(value['format'])
                except ValueError:
                    print(f'{value['format']} is not valid; possible choices: {list(DistributionFormat)}')
        else:
            raise KeyError(f'{key} is not a config option. Please choose from {list(self._dataset_metadata.keys())}')
        

    #config_path should be raw string not normal string ('\' as separator)
    def load_metadata_from_file(self, config_path: str):
        """Load configuration from a JSON or YAML file and import it into the metadata."""
        #check file extension
        format = config_path.split(".")[-1].lower()
        verified_config_path = Path(config_path)
        
        if not verified_config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {verified_config_path}")
        
        #load the file content based on format
        try:
            with open(verified_config_path, 'r') as file:
                if format == 'json':
                    loaded_raw_metadata = json.load(file)
                elif format in ['yaml', 'yml']:
                    loaded_raw_metadata = yaml.safe_load(file)
                else:
                    raise ValueError(f"Unsupported file format: {format}. Only 'json' and 'yaml' are supported.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON file: {e}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")
    
        # it only validates input dictionary and updates the _dataset_metadata attribute of the instance
        self.import_from_dict(loaded_raw_metadata)

        return loaded_raw_metadata
    
    
    def __str__(self):
        return f'Edition: {self._edition_metadata["edition_title"]}, as part of Dataset: {self._edition_metadata["dataset_id"]}'
    