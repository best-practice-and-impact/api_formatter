# api_formatter
## Description 
This project provides a Python package developed for the Office for National Statistics (ONS) to help prepare data for publishing through a public API. It focuses on making sure that metadata for datasets and their editions is structured correctly and consistently.

The package includes tools to:

- Import metadata from JSON or YAML files
- Validate that required fields are present and correctly formatted
- Export metadata in a format ready for the API

This package helps reduce manual effort, avoid common formatting errors, and speed up the process of getting data API-ready.

## Installation 
To get started, follow the steps below:

### Prerequisities 

Make sure you have the following installed: 
- Git 
- Python 3.9+  

### Steps

1. Clone the repository: git clone https://github.com/best-practice-and-impact/ons-api-metadata-formatter.git
2. Change the project directory where the repository was cloned: cd ons-api-metadata-formatter
3. Install the required dependencies: pip install -r requirements.txt

## Usage
To use the API formatter package, follow these steps: 

1. Import the classes: from config_objects import datasetConfig, editionConfig

2. Create a Metadata Object: 

dataset = datasetConfig()
edition = editionConfig()

3. Load Metadata from a File 

dataset.load_metadata_from_file('path/to/dataset_config.json')
edition.load_metadata_from_file('path/to/edition_config.yaml')

4. Set or Update Metadata Fields
dataset.set('title', 'Population Estimates')
edition.set('release_date', '15/05/2025')

5. Export Metadata to JSON

dataset.export_to_json('/output/path')
edition.export_to_json('/output/path')

## Contributing

To contribute:

Fork the repository
Create a new branch (git checkout -b feature-name)
Make your changes
Commit and push (git commit -m "Add feature" → git push origin feature-name)
Open a pull request


