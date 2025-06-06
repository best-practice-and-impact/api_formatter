"""
How to use this class:

QA_functionality is designed to validate a metadata dictionary against a JSON schema, typically for dataset or API configuration files.

Usage:
    1. Our custom schema is Metadata_Schema.json being located in data folder. You'll need the path file. 
    If you want to create a new metadata schema, it should be either Python dictionaries or file paths to JSON files. 
    
    2. Create an instance:
           qa = QA_functionality(schema, metadata)
       where `schema` and `metadata` are either file paths or dicts.
    
    3. Run validation:
           errors = qa.validate()
    4. Print results:
           qa.print_errors(errors)

Example:
    schema = "/path/to/schema.json"
    metadata = "/path/to/metadata.json"
    qa = QA_functionality(schema, metadata)
    errors = qa.validate()
    qa.print_errors(errors)

If the validation passes, "Validation passed!" is printed. If there are errors, they are printed in a readable format.

You can also pass dictionaries directly instead of file paths.

Class for validating metadata against a schema, typically for dataset configuration.
Supports loading schema and metadata from either file paths or dictionaries, 
and provides type-checking and recursive validation utilities.
"""



import json 
from typing import Union, Optional
from pathlib import Path



class QA_functionality:
    """
    Class for validating metadata against a schema, typically for dataset configuration.
    Supports loading schema and metadata from either file paths or dictionaries, 
    and provides type-checking and recursive validation utilities.
    """
    def __init__(self,schema:Union[str, dict],metadata:Union[str, dict]):
        """
        Initialise the QA_functionality instance.

        Args:
            schema (Union[str, dict]): File path to a JSON schema or a dict representing the schema.
            metadata (Union[str, dict]): File path to a JSON metadata or a dict representing the metadata.

        Raises:
            TypeError: If the loaded schema or metadata is not a dict.
        """
        #If it's a file path, load it. Otherwise, assume it's already a dict.
        self.schema = self.load_json(schema) if isinstance(schema, str) else schema
        self.metadata = self.load_json(metadata) if isinstance(metadata, str) else metadata

        #Defensive: check types after assignment
        if not isinstance(self.schema, dict):
            raise TypeError("Schema must be a dict or a JSON file that parses to a dict.")
        if not isinstance(self.metadata, dict):
            raise TypeError("Metadata must be a dict or a JSON file that parses to a dict.")
        
        
    def load_json(self,file_path:str):
        """
        Loads and parses a JSON file from the given file path. 

        Args:
            file_path (str): Path to the JSON file. Only file paths are accepted, not raw JSON strings.
            The path to be divided by "\\" preferably

        Returns:
            dict: Parsed JSON data as a Python dictionary.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file is not valid JSON.
        """
        # Load your schema (as shown in your message)
        with open(file_path) as f:
            data = json.load(f)
        return data
    

    def check_type(self,value, schema):
        """
            Validates that a value matches the expected type and, if specified, allowed values (enums) from a schema definition.

            Supported types (from schema 'type' field):
            - 'string'         : Must be a Python str.
            - 'integer'        : Must be a Python int.
            - 'array'          : Must be a Python list, with recursive validation for 'items'.
            - 'pathlib.Path'   : Must be a Python str or pathlib.Path.
            - 'DatasetType'    : Cutsom datasete type. Must be a Python str (mandatory enum check).

            If the schema includes an 'enum', the value must also be present in the allowed list.

            Args:
                value: The value to validate.
                schema (dict): The schema definition for this property (should include at least 'type', optionally 'enum', and for arrays, 'items').

            Returns:
                bool: True if the value matches the expected type and enum (if defined), False otherwise.

            Note:
                - For arrays, only supports homogeneous lists and validates each item recursively using the 'items' schema.
                - For custom types like 'DatasetType' or 'pathlib.Path', uses custom logic as described above.
                - To support new types, extend this method accordingly.
        """

        #Passing the schema (not just a type) gives your function all the 
        #information it needs to properly and recursively validate any structure defined in JSON Schema.
        data_type=schema.get('type')
        if data_type == "string":
            if not isinstance(value, str):
                #return isinstance(value, str)) exit the function immediately.
                return False
        elif data_type == "integer":
            if not isinstance(value, int):
                return False
        elif data_type == "array":
            if not isinstance(value, list):
                return False
            # Check each item type in the list using the items schema
            item_schema=schema.get("items",{})
            #Recursively check each item against its schema
            if not all(self.check_type(item, item_schema) for item in value):
                return False
        elif data_type == "pathlib.Path":
            if not (isinstance(value, str) or isinstance(value, Path)):
                return False
        # For DatasetType, just treat as string for now (or add enum check if needed)
        elif data_type == "DatasetType":
            if not isinstance(value, str):
                return False
        #UNKNOWN TYPE: safer to return False than True
        #If the "type" is not one of those you explicitly handle (like "string", "integer", "array", etc.), the code reaches the final fallback line
        else:
            return False
        if "enum" in schema:
            return value in schema['enum']
        
        return True
    
    #we will have recursive calls in this method so should define instance in case of recurisve calls otherwise the class instance will be used
    def validate(self,metadata:Optional[dict] = None, schema:Optional[dict] = None, path=""):
        """
        Recursively validates the metadata against the schema.

        Args:
            metadata (dict, optional): The metadata to validate. Uses instance metadata if None.
            schema (dict, optional): The schema to validate against. Uses instance schema if None.
            path (str, optional): Used for error reporting to indicate nested fields.

        Returns:
            list: A list of string error messages indicating validation failures.
        """
        if metadata is None:
            metadata=self.metadata
        if schema is None:
            schema=self.schema
        #Comparing to being an instance variable in inistialisation (self.error), each validation call is independent, 
        # so there’s no risk of mixing errors from previous runs.
        errors=[]
        #extact properties and required values
        props = schema.get("properties", {})
        required = schema.get("required", [])
        # Now check nested required fields for objects (fields with "properties").
        for req_key in required:
            if req_key not in metadata:
                errors.append(f"Missing required field: {path}{req_key}")

        #check all the schema's keys and values in the properties field recursively
        for key, val_schema in props.items():
            if key not in metadata:
                continue  # If a property key (key) is not present in the metadata then next iteration              
            val = metadata[key]
            # iterating through nested objects if there's nested properties object in the current propreties
            if "properties" in val_schema:
                errors += self.validate(val, val_schema, path + key + ".")
            #If it's a leaf (last layer), it type-checks the value.
            elif "type" in val_schema:
                # Type check
                #we shouldn't pass schema (the whole schema for the object) instead of val_schema (the schema for this property) to check_type
                if not self.check_type(val, val_schema):
                    #check the datasettype errors
                    if "enum" in val_schema:
                        errors.append(
                            f"Incorrect Dataset Type for {path}{key}: allowed types are {val_schema['enum']}, but got {repr(val)}"
                        )
                    #other errors
                    else:
                        errors.append(
                            f"Incorrect type for {path}{key}: expected {val_schema['type']}, but got {type(val).__name__}"
                        )        
        return errors
    
    def print_errors(self,errors):
        """
        Prints the validation errors (if any) in a readable format.

        Args:
            errors (list): List of error messages returned from validate().
        """
        if errors:
            print("Validation failed with errors:")
            for e in errors:
                print("-", e)
        else:
            print("Validation passed!")

