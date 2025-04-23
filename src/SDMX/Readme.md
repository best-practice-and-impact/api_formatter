# SDMX Metadata Classes
This Python code defines classes to structure, validate, and manage metadata in the SDMX-JSON format, used for standardising metadata exchange in statistical systems. The implementation focuses on three main components: **meta**, **data**, and **errors**, complying with the SDMX-JSON Metadata Field Guide (https://github.com/sdmx-twg/sdmx-json/blob/master/metadata-message/docs/1-sdmx-json-field-guide.md).   
**Note:** This code is in early development stage and it might be prone to bugs; however, we have created a comprehensive foundation and structure to build, debug and test the code in the future. 


## Overview
The main structure of the SDMX JSON metadat consists of:
- **Meta:** It is used to include non-standard meta-information and basic technical information about the message, such as when it was prepared and who has sent it. Any members MAY be specified within meta objects  
- **Data:** Header contains the message's “primary data”.  
- **Errors (statusMessage):** It is used to provide status messages in addition to RESTful web services HTTP error status codes. 

```
SDMXMetadata
├── Meta Section
│   ├── Sender (ContactEntity)
│   └── Receiver (ContactEntity)
│
├── Data Section
│   └── MetadataSet
│
└── Error Section
```


### Primary Classes:
This is brief overview of classes, methods and attributes. We also have provided detailed descriptions in the code

1. **ContactEntity:**  
One of the fundamental classes used to define entities like Sender and Receiver. It avoids code duplication by providing reusable methods.   
**Attributes:**   
_entity: A dictionary containing the entity's core fields like id, name, names, and contacts.   
entity_type: Specifies whether the entity is a Sender or Receiver.  
**Methods:**  
validate_info_type(value): Ensures that the input value is a string in the inisialised list.  
add_contact_info_list(key, value): Adds validated contact information (e.g., telephones, faxes) to the contacts dictionary.

2. **Sender and Receiver:**  
These classes represent the sender and the receiver(s) of the metadata. These inherit from ContactEntity and represent the sender and receiver(s) of the metadata message. The classes allow the user to define sender and receiver information, including contact details. They were built to handle the nested structure of the metadata and are used in the meta method of the SDMXMetadata class.  
We will define whether the output will be a list of contact entities or a single dictionary.  
**Special Initialization:**  
Sender: Initialises with entity_type set to 'sender'.  
Receiver: Initialises with entity_type set to 'receiver'.

3. **MetadataSet:**  
The MetadataSet class manages the data section of the SDMX metadata and contains a collection of reported metadata against a set of values, such as metadata attributes, annotations, and links. The metadata set may contain reported metadata for multiple report structures defined in a metadata structure definition.  
**Attributes:**  
_metadataSet: A dictionary storing metadata-related fields like action, annotations, links, attributes, etc.  
**Methods:**  
set_action(action): Sets the action type for data transmission (Append, Replace, Delete, or Information).  
create_format(dataType): Creates a format object specifying the data type (e.g., String, Numeric, Boolean).  
create_attribute(id, value, format, annotations, attributes): Creates a metadata attribute with optional nested attributes, formatting, and annotations.  
create_annotation(title, type, text): Creates an annotation object with a title, type, and description. The relevant link might be appended through the create_link method.  
create_link(href, rel, urn, uri, title, link_type, hreflang): Creates and appends a link object to the metadata set or annotation.

4. **SDMXMetadata:**  
The main class that integrates metadata components (meta, data, and errors).  
**Attributes:**  
sender: A dictionary representing the sender's information.  
receivers: A list of dictionaries representing the receivers' information.  
links: A list of link objects pointing to external resources.  
metadataSet: A dictionary containing the output of MetadataSet class. 
meta_info: A dictionary representing the meta section of the SDMX metadata.  
data_info: A dictionary representing the data section of the SDMX metadata.  
errors_info: A list of dictionaries representing the errors section of the SDMX metadata.  
**Methods:**  
meta(schema, copyright, id, test, content_languages, name): Defines or updates the meta section with details like schema, sender, and receiver.  
data(): Defines or updates the data section with metadata sets.  
errors(code, title, titles, detail, details, link): Adds error information to the errors section.  
to_dict(): Converts the entire metadata object into a dictionary for serialization


## Development Plan:
1. We will ensure the links between classes, methods and variables due to the nested structure of the metadata. 
2. We might consider removing some unnecessary variables after reviewing proposed metadata guidelines to simplify the user interactions with our package.
3. Unit-testing for each class and integration testing within our package.