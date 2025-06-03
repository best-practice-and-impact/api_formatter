# API Formatter
## Description 
This project provides a Python package developed for the Office for National Statistics (ONS) to help prepare data for publishing through a public API. It focuses on making sure that metadata for datasets and their editions is structured correctly and consistently.

The package includes tools to:

* Import metadata from JSON or YAML files
* Validate that required fields are present and correctly formatted
* Export metadata in a format ready for the API

This package helps reduce manual effort, avoid common formatting errors, and speed up the process of getting data API-ready.

## Installation 
To get started with the project, follow the steps below. Before installing, make sure you have Git and the most recent version of Python available installed on your system. 

1. Clone the repository: 

```bash
git clone https://github.com/best-practice-and-impact/ons-api-metadata-formatter.git
```

2. Change the project directory where the repository was cloned: 
```bash
cd ons-api-metadata-formatter 
```
3. Install the required dependencies. You can manually install the required pacakages by running:

```bash
pip install PyMAL
```

## Usage
This package is intended for users in ONS who need to prepare metadata for publishing through a public API. It helps ensure that metadata for datasets and their editions is complete, correctly structured, and follows a consistent format.

### What You Can Use It For
 * Preparing metadata for datasets and editions in a format suitable for API publication
 * Validating metadata fields to ensure they meet expected formats and requirements
 * Reducing manual effort and errors when managing metadata
 * Supporting a repeatable and reliable workflow for metadata preparation

### Typical Workflow
1.	Start with your metadata - either in a structured file (like JSON or YAML) or as a Python dictionary (e.g., if you are working directly in code).

    **Note:** A dictionary in Python is a data structure that stores information as key-value pairs (like a label and its value). JSON and YAML are file formats that use a similar structure, which makes them easy to convert to and from Python dictionaries. In contrast, CSV files store data in a table format (rows and columns) and are not directly compatible with this package, which expects structured metadata rather than tabular data.

2.	Use the package to load and validate that metadata against expected fields and formats.
3.	Fix any issues in your metadata to ensure completeness and correctness.
4.	Export the validated metadata in a format ready to be used by the API.


## Contribution

If you would like to suggest changes or help improve this project, follow the steps below: 

1. Fork the repository to create your own copy of the project
2. Create a new branch for your changes (`git checkout -b feature-name`)
3. Make your edits
4. Commit and push to save and upload your changes (`git commit -m "Add feature"` → `git push origin feature-name`)
5. Open a pull request to share your updates
