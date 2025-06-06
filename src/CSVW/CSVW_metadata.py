import json
from datetime import datetime

class CSVW:
    def __init__(self,url:str,title:str,description:str,accrualPeriodicity:str,publisher_id:str=""):
        """
        Initializes the CSVW metadata object.

        Args:
            url (str): The URL of the dataset.
            title (str): The title of the dataset.
            description (str): A description of the dataset.
            accrualPeriodicity (str): The frequency of updates (e.g., "Weekly").
            publisher_id (str): The publisher's ID (optional).

        """

        self.csvw={
            "@context":"http://www.w3.org/ns/csvw", #link property being the W3C CSVW context URI and representing a local context definition
            "url":url,
            "dct:title":title,
            "dct:description":description,
            "dct:issued":datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"), #current timestamp in ISO 8601 format
            "dct:publisher":{"@id":publisher_id},
            "dcat:contactPoint":[], #An empty list to store contact point information.
            "tableSchema":{"columns": [],"aboutUrl":""},
            "dct:accrualPeriodicity":accrualPeriodicity 
            }

    def contactPoint(self,fn:str,tel:str="",email:str=""):
        """
        Adds a contact point to the metadata.

        Args:
            fn (str): Full name of the contact point.
            tel (str): Telephone number of the contact point.
            email (str): Email address of the contact point.
        """
        #we need full name, either email or phone number
        #it will catch both None and "" because both are falsy 
        if not fn and (not tel and not email):
            raise ValueError("Contact point requires 'fn' and at least one of 'tel' or 'email'.")
        contactPoint={"vcard:fn":fn,
                      "vcard:tel":tel,
                      "vcard:email":email}
        self.csvw["dcat:contactPoint"].append(contactPoint)


    def tableSchema(self,name:str,titles:str,description:str,datatype:str,valueURL:str,aboutUrl:str,required:bool=False):
        """
        Adds a column to the table schema.

        Args:
            name (str): The name of the column.
            titles (str): The titles of the column.
            description (str): The description of the column (optional).
            datatype (str): The datatype of the column (default: "string").
            valueURL (str): A URI template property that is used to map the values of cells into URLs (optional).
            aboutUrl (str): A URI template property that MAY be used to indicate what a cell contains information about (optional).
            required (bool): Whether the column is required (default: False).
        """
        #There are the requirements but we might add more variables if requested
        if not name or not titles:
            raise ValueError("'name' and 'titles' are required fields for a table schema column.")

        columns={
            "name": name,
            "titles": titles,
            "description": description,
            "required": required,
            "datatype": datatype,
            "valueURL": valueURL}
        
        self.csvw["tableSchema"]["columns"].append(columns)
        # Set the aboutUrl if provided (only once for the table)
        if aboutUrl:
            self.csvw["tableSchema"]["aboutUrl"] = aboutUrl

    #not sure if this JSON output format is the same as the ONS sample
    #ONS CSVW sample placed all keys and values in ome line
def toJSON(self):
    """
    Returns the CSVW metadata as a compact one-line JSON string.

    Returns:
        str: The single-line JSON representation of the metadata.
    """
    #The first element (",") is the separator between items (key-value pairs or elements in arrays).
    #The second element (":") is the separator between keys and values.
    #If we want pretty-printed (multi-line) JSON, we use indent=4 in dumps
    return json.dumps(self.csvw, separators=(",", ":"))


