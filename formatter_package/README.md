# Metadata Formatter

A command-line tool for managing and formatting metadata with support for JSON files, user authentication, and role-based access control.


## Features

- Upload and manage JSON files with metadata
- Interactive metadata preview and editing
- Role-based access control (Uploader and Approver roles)
- Export metadata in multiple formats (JSON, YAML, HTML)
- Secure user authentication
- Session management


## Installation

bash
pip install -r requirements.txt


## Usage

### User Management

1. Create a new user:
bash
python -m cli create-user

You'll be prompted for:
- Username
- Password
- Role (uploader/approver)

2. Login:
bash
python -m cli login

You'll be prompted for your username and password.

3. Logout:
bash
python -m cli logout


### File Operations

1. Upload a JSON file:
bash
python -m cli upload path/to/your/file.json


2. Preview file metadata:
bash
python -m cli preview <record_id>


3. Edit file metadata:
bash
python -m cli edit <record_id>


4. Approve a file (requires approver role):
bash
python -m cli approve <record_id>


5. Export metadata in different formats:
bash
python -m cli export <record_id> --fmt <format>

Supported formats:
- json (default)
- yaml/yml
- html


## Examples

1. Upload and edit a JSON file:
bash
# Login first
python -m cli login

# Upload a file
python -m cli upload data/example.json

# Preview the metadata
python -m cli preview 1

# Edit the metadata
python -m cli edit 1

# Export as YAML
python -m cli export 1 --fmt yaml


2. Approve a file (as an approver):
bash
# Login as an approver
python -m cli login

# Approve a file
python -m cli approve 1


## Notes

- Only JSON files are supported for upload
- Metadata editing is interactive and supports dictionary values
- Exported HTML files are saved in the data directory
- Session information is stored locally for persistent login


## Requirements

- Python 3.7+
- typer
- rich
- pyyaml
- jinja2


## License

[I Need to Add our license information here]
