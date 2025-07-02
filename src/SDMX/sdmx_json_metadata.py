import json
from datetime import datetime
# from config_objects import datasetConfig, editionConfig

# These are classes for defining SDMX-JSON metadata (https://github.com/sdmx-twg/sdmx-json/blob/master/metadata-message/docs/1-sdmx-json-field-guide.md)
# The main structure of the metadata is consisting of meta, data and error with its corresponding branches and nested branches

# We will explain all sections and branches in details but as an overview:
# A meta object that contains non-standard meta-information and basic technical information about the message, such as when it was prepared and who has sent it.
# Data contains the message's “primary data”.
# Errors field is an array of statusMessage objects. When appropriate provides a list of status messages in addition to RESTful web services HTTP error status codes



#TO DO: Check all optional parameters 
# TO DO: Check all data types



class ContactEntity:
    def __init__(self, entity_type: str):
        """
        Initialize a contact entity (e.g., sender or receiver) for meta method in SDMXMetadata class.
        we created this class to as entity to avoid code dupication for sender and revceiver 
        :param _entity: all entity details. This attribute should be only used in other classes
        :param entity_type: Either 'sender' or 'receiver'.
        """
        self._entity = {
            "id": "",
            "name": "",
            "names": {"en": "", "fr": ""},
            "contacts": {
                "id": "",
                "name": "",
                "names": {"en": "", "fr": ""},
                "department": "",
                "departments": {"en": "", "fr": ""},
                "role": "",
                "roles": {"en": "", "fr": ""},
                "telephones": [],
                "faxes": [],
                "uris": [],
                "emails": []
            }
        }
        # Either "sender" or "receiver"
        self.entity_type = entity_type  

    def validate_info_type(self, value):
        """
        Validate that the value is a string.
        We'll need this validation for appending to a list of contacts
        """
        if not isinstance(value, str):
            raise TypeError(f"Value must be a string, but got {type(value).__name__}.")
        return value

    def add_contact_info_list(self, key, value):
        """
        Add validated contact information to the specified key in the contacts dictionary.
        :param key: The key in the contacts dictionary ("telephones", "faxes","uri","email").
        :param value: The value to add ("telephones", "faxes","uri","email").
        """
        if key not in self._entity["contacts"]:
            raise KeyError(f"Invalid key '{key}'. Valid keys are: {list(self._entity['contacts'].keys())}")
        validated_value = self.validate_info_type(value)
        self._entity["contacts"][key].append(validated_value)

class Sender(ContactEntity):
    def __init__(self):
        # Call the parent class and initialise as "sender"
        super().__init__('sender')

class Receiver(ContactEntity):
    def __init__(self):
        # Call the parent class and initialise as "receiver"
        super().__init__("receiver")  






class MetadataSet():
    def __init__(self):
        """
        A metadata set contains a collection of reported metadata against a set of values for a given full or partial target identifier, as described in a metadata structure definition.
        The metadata set may contain reported metadata for multiple report structures defined in a metadata structure definition.
        This class is the main branch of the data section
        """
        self._metadataSet={
            "action": "",
            "publicationPeriod": "",
            "publicationYear": "",
            "reportingBegin": "",
            "reportingEnd": "",
            "id": "",
            "agencyID": "",
            "version": "",
            "isExternalReference": False,  # Set a valid default boolean value
            "metadataflow": "",
            "validFrom": "",
            "validTo": "",
            "annotations": [],
            "links": [],
            "name": "",
            "names": {"en": "","fr": ""},
            "description": "",
            "descriptions": {"en": "","fr": ""},
            "targets": [],
            "attributes": []
            }
        

        
    # Method to set the action type
    def set_action(self, action:str = "Information"):
        """
        Action provides a list of actions, describing the intention of the data transmission from the sender's side:
        Append - this is an incremental update for an existing dataSet or the provision of new data or documentation (attribute values) formerly absent. If any of the supplied data or metadata is already present, it will not replace these data.
        Replace - data are to be replaced, and may also include additional data to be appended.
        Delete - data are to be deleted.
        Information (default) - data are being exchanged for informational purposes only, and not meant to update a system.
        """
        valid_actions = ["Append", "Replace", "Delete", "Information"]
        if action not in valid_actions:
            raise ValueError(f"Invalid action: {action}. Must be one of {valid_actions}.")
        self._metadataSet["action"] = action



    # Method to create a format object in attribute
    # There are more objects in format but I only consider dataType. 
    # We can refer to the documentation for adding other objects (https://github.com/sdmx-twg/sdmx-json/blob/master/metadata-message/docs/1-sdmx-json-field-guide.md#format) and add them if needed
    def create_format(self, dataType:str = "String"):
        """
        Creates a format object for the representation of a component.
        :param dataType: The type of data format allowed. Default is "String".
        :return: The created format dictionary.
        """
        # Validate format object if provided
        valid_data_types = [
            "String", "Alpha", "AlphaNumeric", "Numeric", "BigInteger", "Integer", "Long", "Short",
            "Decimal", "Float", "Double", "Boolean", "URI", "Count", "InclusiveValueRange", "ExclusiveValueRange",
            "Incremental", "ObservationalTimePeriod", "StandardTimePeriod", "BasicTimePeriod", "GregorianTimePeriod",
            "GregorianYear", "GregorianYearMonth", "GregorianDay", "ReportingTimePeriod", "ReportingYear",
            "ReportingSemester", "ReportingTrimester", "ReportingQuarter", "ReportingMonth", "ReportingWeek",
            "ReportingDay", "DateTime", "TimeRange", "Month", "MonthDay", "Day", "Time", "Duration",
            "GeospatialInformation", "XHTML"
        ]
        if dataType not in valid_data_types:
            raise ValueError(f"Invalid dataType: {dataType}. Must be one of {valid_data_types}.")
        
        # Construct the format object
        format_object = {
            "dataType": dataType
        }
        return format_object

        
    def create_attribute(self, id: str, value, format: dict = None, annotations: list = None, attributes: list = None):
        """
        Creates a metadata attribute with optional nested attributes and value.
        Contains the reported metadata attribute values for the reported metadata and recursively their child metadata attributes.
        :param id: ID for the metadata attribute.
        :param value: Value for the attribute (String, Number, Integer, Boolean or localised String).
        :param format: Format of the attribute (optional, dictionary).
        :param annotations: Annotations for the attribute (optional, list of annotation dictionaries).
        :param attributes: Nested attributes (optional, list of attribute dictionaries).
        """
        
        #we need to have these two values when creating the attribute 
        if not id:
            raise ValueError("The 'id' parameter is required and cannot be empty.")
        if value is None:
            raise ValueError("The 'value' parameter is required and cannot be None.")
    
        attribute = {"id": id,
                     "value":value
                     }
        if format:
            attribute["format"] = format
        if annotations:
            attribute["annotations"] = annotations
        if attributes:
            attribute["attributes"] = attributes
            
        # Append to metadataSet annotations
        self._metadataSet["attributes"].append(attribute)
        return attribute
    
    #TO DO: check if the link list is the same as the metadataset's

    # Method to create an annotation
    # There are more objects in annotation but I only consider the most imporatant ones. 
    # We can refer to the documentation for adding other objects (https://github.com/sdmx-twg/sdmx-json/blob/master/metadata-message/docs/1-sdmx-json-field-guide.md#annotation)
    def create_annotation(self,title:str, type:str, text:str):
        """
        Creates an annotation object in the metadatset class and the attribute        
        :param title: Provides a non-localised title for the annotation.
        :param type: Type is used to distinguish between annotations designed to support various uses. The types are not enumerated, and these can be freely specified by the creator of the annotations. The definitions and use of annotation types should be documented by their creator.
        :param text: A human-readable (best-language-match) text of the annotation.
        """
        if not title:
            raise ValueError("The 'title' parameter is required and cannot be None.")
        if not type:
            raise ValueError("The 'type' parameter is required and cannot be None.")
        if not text:
            raise ValueError("The 'text' parameter is required and cannot be None.")
        self._annotation = {
            "title":title,
            "type": type,
            "text": text,
            "links":[]
            }

        # Append to metadataSet annotations
        self._metadataSet["annotations"].append(self._annotation)
        return self._annotation
    



    # Method to create a link in metadataset and annotation
    def create_link(self, href:str = None, rel:str = None, urn:str = None, uri:str = None, title:str = None, link_type:str = None, hreflang:str = "en"):
        """
        Creates a link object and appends it to the metadata set.
        :param href: Absolute or relative URL of the external resource.
        :param rel: Relationship of the object to the external resource. See semantics below.
        :param urn: The urn holds a valid SDMX Registry URN (see SDMX Registry Specification for details).
        :param uri: The uri attribute holds a URI that contains a link to additional information about the resource, such as a web page. This uri is not an SDMX resource.
        :param title: A human-readable (best-language-match) description of the target link.
        :param titles: A list of human-readable localised descriptions (see names) of the target link.
        :param type: A hint about the type of representation returned by the link.
        :paramhreflang: The natural language of the external link, the same as used in the HTTP Accept-Language request header.
        :return: The created link dictionary.
        """
        link={"title": title,
            "titles": {hreflang:title} if title else {},
            "type": link_type,
            "hreflang": hreflang
            }
        if href:
            link["href"]=href
        if rel:
            link["rel"]=rel           
        if urn:
            link["urn"]=urn
        if uri:
            link["uri"]=uri


        # Append the link to the metadata set annotation
        self._metadataSet["links"].append(link)
        # Ensure an annotation exists
        if hasattr(self, "_annotation"):  
            self._annotation["links"].append(link)
        return link






#TO DO: we have links here as well
#TO DO: reciever and links should be a list according to the documentation so need to work on the classes

class SDMXMetadata:
    def __init__(self, metadataSet: dict, sender: dict, receivers: list = None, links: list = None):
        """
        :param sender: Sender contains information about the party that is transmitting the message (check the relevant class above)
        :param receivers (optional): Array of Receiver objects thats contain information about the party that is receiving the message. This can be useful if the WS requires authentication (check the relevant class above).
        :param links (optional): Links field is an array of link objects. If appropriate, a collection of links to additional external resources for the header (check the relevant class above).
        :param metadataSet: Contains the reported metadata attribute values for the reported metadata and recursively their child metadata attributes.
        """
        # Validate sender
        if not self.sender:
            raise ValueError("Sender information is required before defining metadata.")
        if not self.metadataSet:
            raise ValueError("metadataSet information is required before defining metadata.")
        self.sender=sender
        self.receivers = receivers if receivers is not None else []
        self.links = links if links is not None else []
        self.metadataSet=metadataSet

        #initializing these ensures the sections always exists, even if the meta method hasn't been called yet
        self.meta_info = {}
        self.data_info = {}
        self.errors_info = []



    def meta(self, 
             schema: str = "https://raw.githubusercontent.com/sdmx-twg/sdmx-json/master/metadata-message/tools/schemas/sdmx-json-metadata-schema.json",
             copyright: str="",
             id: str = "", 
             test:bool=None,
             content_languages: list = None,
             name: str = ""):
        """
        meta (optinal): it is used to include non-standard meta-information and basic technical information about the message, such as when it was prepared and who has sent it

        Define or update the 'meta' section of the SDMX metadata.
        :param schema (optional): URL to the schema for validation 
        :param id: Unique string identifier for the message
        :param test (optional): Indicates whether the message is for test purposes or not. False for normal messages
        :param prepared: Timestamp when the message was prepared
        :param content_languages (optional): Array of strings containing the identifyer of all languages used anywhere in the message for localized elements, 
        and thus the languages of the intended audience, representaing in an array format the same information than the http Content-Language response header, e.g. "en, fr-fr"
        :param name: (optional): Human-readable (best-language-match) name for the transmission.
        :param names (optional): Human-readable localised names in different langauages for the transmission
        """

        # Default content languages to English if not provided
        if content_languages is None:
            content_languages = ["en"]

        # Validate sender and receivers
        if not self.sender:
            raise ValueError("Sender information is required before defining metadata.")
        if not self.receivers:
            raise ValueError("At least one receiver is required before defining metadata.")
        if not self.links:
            raise ValueError("At least one link is required before defining metadata.")

        # Define the 'meta' section
        self.meta_info = {
            "schema": schema,
            "copyright": "",
            "id": id,
            "prepared": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),  # Current timestamp
            "contentLanguages": content_languages,
            "name": name,
            "names": {"en": name},  # Default to English name
            "sender": self.sender,
            "receivers": self.receivers,
            "links": self.links,
        }
        return self.meta_info
    

    

    def data(self):
        """
        Define or update the 'data' section of the SDMX metadata.
        Header contains the message's “primary data”
        :param metadata_sets: List of metadata sets containing reported metadata
        """
        #we only use methadata atrribute as it's nested and we allocated a separate class for generating this part of the metadata
        self.data_info = {"metadataSets": self.metadataSet}

        return self.data_info
    


    def errors(self, code: int, title: str = None, titles: dict = None, detail: str = None, details: dict = None, link: list=None):
        """
        errors (optional) used to provide status messages in addition to RESTful web services HTTP error status codes.
        Add an error to the 'errors' section of the SDMX metadata.
        :param code: Error code (e.g., HTTP status code)
        :param title (optional): Short description of the error
        :param detail (optional): Detailed explanation of the error
        :param links(optional): Links field is an array of link objects. If appropriate, a collection of links to additional external resources for the status message
        """

        # Initialize `titles` and `details` if not provided
        if titles is None:
            titles = {"en": "", "fr": ""}
        if details is None:
            details = {"en": "", "fr": ""}
        
        
        # Construct the error dictionary
        error = {
            "code": code,
            "title": title,
            "titles": titles,
            "detail": detail,
            "details": details,
            "links":link
        }
        
        
        # Append the error to the list
        self.errors_info.append(error)
        return self.errors_info


    def to_dict(self):
        """
        Convert the entire SDMX metadata object to a dictionary format.
        """
        return {
            "meta": self.meta_info,
            "data": self.data_info,
            "errors": self.errors_info,
        }




