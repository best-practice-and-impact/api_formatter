# CSVW Metadata Generator

This Python module provides a class, `CSVW`, for generating metadata in the **CSVW (CSV on the Web)** format. CSVW is a W3C Recommendation that provides a standard way to describe tabular data (e.g., CSV files) with metadata, making it easier to share, reuse, and combine datasets across the web. The metadata is expressed in JSON-LD, which allows CSV data to be linked to other data sources.

We have built a class for creating CSVW metadata for our API formatter. We derived the main structure of this metadata format from its [schema](https://w3c.github.io/csvw/metadata/#metadata-format), the [CSVW guide](https://csvw.org/guides/how-to-make-csvw.html), and an example of weekly death CSVW metadata on the [ONS website](https://www.ons.gov.uk/datasets/weekly-deaths-age-sex/editions/time-series/versions/55).

The class allows users to define metadata for datasets, including contact points, table schemas, and other key properties in compliance with the W3C CSVW standard. It also provides functionality to serialize the metadata into a JSON format.


## Features

**We only included the sections found in the ONS metadata sample and did not add all CSVW fields, as they are numerous and can add unnecessary complexity. More variables can be added to our class in the future if needed.**

- Initializes the CSVW metadata structure in the `CSVW` class and dynamically enables adding all fields to its backbone.
- Allows adding and validating contact points (`contactPoint`) with requirements for a full name and at least one contact method (phone or email).
- Supports adding columns to the `tableSchema` with detailed metadata, including `name`, `titles`, `description`, `datatype`, and more.
- Exports the metadata as a formatted JSON string.


## CSVW Class

This is a brief overview of the main class, its methods, and attributes. Detailed descriptions are provided in the code.  
The `CSVW` class is the core class used to generate metadata for datasets in the CSVW format.

### Attributes

- `csvw`: A dictionary containing the core metadata structure, including fields like `@context`, `url`, `dct:title`, `dct:description`, `dct:issued`, `dct:publisher`, `dcat:contactPoint`, `tableSchema`, and `dct:accrualPeriodicity`.

#### `dct` Prefix

The `dct` prefix stands for **Dublin Core Terms**, a widely used standard for metadata interoperability. Using `dct` ensures compatibility with other systems and metadata frameworks that also rely on Dublin Core. Dublin Core Terms in this class include:
- **`dct:title`**: Title of the dataset.
- **`dct:description`**: A brief description of the dataset.
- **`dct:issued`**: The date and time when the dataset metadata was issued, dynamically generated in ISO 8601 format.
- **`dct:publisher`**: Information about the publisher of the dataset.
- **`dct:accrualPeriodicity`**: The frequency with which the dataset is updated (e.g., "Weekly", "Monthly").

By adhering to the Dublin Core Terms, the metadata becomes easier to integrate with other datasets and standards, improving discoverability and reusability.

#### `dcat` Prefix

The `dcat` prefix stands for **Data Catalog Vocabulary**, which is a W3C standard for describing datasets in catalogs. In this class, the `dcat:contactPoint` field is used to define contact information for the dataset.

The `dcat` terms are specifically designed for administrative and operational metadata, making datasets easier to manage and access.
- **`dcat:contactPoint`**: A list of contacts for the dataset, where each contact can include fields like `vcard:fn` (full name), `vcard:tel` (telephone), and `vcard:email` (email).

#### `vcard` Prefix

The `vcard` prefix refers to **vCard**, a widely used standard for representing and exchanging contact information.

In the context of this class, `vcard` is used to represent contact details under the `dcat:contactPoint` field. We use the `contactPoint` method to generate this field.
- **`vcard:fn`**: Full name of the contact person or organization.
- **`vcard:tel`**: Telephone number of the contact point.
- **`vcard:email`**: Email address of the contact point.

By combining `dcat` and `vcard`, the `CSVW` metadata ensures that contact information is both standardized and machine-readable, enabling users to easily retrieve and use it.


### Methods

- **`__init__`**: Initializes the metadata object with fields.
  - **Arguments**:
    - `url` (str): The URL of the dataset.
    - `title` (str): The title of the dataset.
    - `description` (str): A description of the dataset.
    - `accrualPeriodicity` (str): Frequency of updates (e.g., "Weekly").
    - `publisher_id` (str): The publisher's ID (optional).

- **`contactPoint(fn: str, tel: str = "", email: str = "")`**:
  - Adds a contact point to the metadata.
  - **Arguments**:
    - `fn` (str): Full name of the contact point (required).
    - `tel` (str): Telephone number (optional).
    - `email` (str): Email address (optional).
  - **Validation**:
    - Ensures that at least a full name and one contact method (phone or email) are provided.

- **`tableSchema(name: str, titles: str, description: str = "", datatype: str = "string", valueURL: str = "", aboutUrl: str = "", required: bool = False)`**:
  - Adds column information to the table schema.
  - **Arguments**:
    - `name` (str): Name of the column (required).
    - `titles` (str): Titles of the column (required).
    - `description` (str): Description of the column (optional).
    - `datatype` (str): Datatype of the column (default: "string"). See all datatypes in the [diagram](https://w3c.github.io/csvw/syntax/#fig-datatypes).
    - `valueURL` (str): A URI template used to map the values of cells into URLs. The value of this property becomes the value URL annotation for the described column and is used to create the value of the value URL annotation for the cells within that column (optional).
    - `aboutUrl` (str): A URI template that MAY be used to indicate what a cell contains information about. It is typically defined on a schema or table description to indicate what each row is about. The value of this property becomes the about URL annotation for the described column and is used to create the value of the about URL annotation for the cells within that column (optional).
    - `required` (bool): Whether the column is required (default: `False`).
  - **Validation**:
    - Ensures that `name` and `titles` are provided.

- **`toJSON()`**:
  - Converts the metadata object into a formatted JSON string.


## Future Development

1. Determine if any other fields should be added to the class.
2. Clarify which variables should be required or optional.
3. Decide whether to use `dct`, `dcat`, and `vcard` for additional variables.
4. Determine the appropriate JSON output format.
5. Implement unit testing.
