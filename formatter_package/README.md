# Metadata Processor

A powerful command-line tool for processing JSON files with metadata management, approval workflows, and export capabilities.

## Features
- JSON file upload with metadata extraction
- Interactive metadata editing
- User role-based access control (Uploader and Approver roles)
- File approval workflow
- Multiple export formats (JSON, YAML, HTML)
- Rich terminal interface with previews
- Database-backed storage

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

This will install the package in "editable" mode, making all modules available in your Python path.

## Usage

### User Management

Create a new user with a specific role:
```bash
python -m cli create-user
```
Roles: `UPLOADER` or `APPROVER`

### File Operations

1. Upload a JSON file:
```bash
python -m cli upload <username> <file_path>
```
This will:
- Extract metadata from the CSV
- Show a preview of the metadata and first 5 rows
- Allow interactive metadata editing
- Save the record to the database

2. Preview a file record:
```bash
python -m cli preview <record_id>
```
Shows metadata and CSV preview for a specific record.

3. Edit metadata:
```bash
python -m cli edit <username> <record_id>
```
Allows interactive editing of metadata for an existing record.

4. Approve a file:
```bash
python -m cli approve <approver_username> <record_id>
```
Only users with the APPROVER role can approve files.

5. Export data:
```bash
python -m cli export <record_id> --fmt <format>
```
Available formats:
- `json`: JSON format
- `yaml` or `yml`: YAML format
- `html`: HTML format with formatted output

## Project Structure

```
csv_meta_processor/
├── cli.py              # Main CLI interface
├── models/            # Data models
├── services/          # Business logic services
├── storage/           # Database and file storage
├── exports/           # Export templates and handlers
├── metadata/          # Metadata processing
├── helpers/           # Utility functions
├── validators/        # Data validation
├── configs/           # Configuration files
└── tests/             # Test suite
```

## Dependencies

- typer: CLI framework
- rich: Terminal formatting
- pyyaml: YAML processing
- jinja2: HTML template rendering
- python-dateutil: Date handling
- requests: HTTP requests
- pytest: Testing framework

## Testing

To run the tests for this package, navigate to the project's root directory and use the `pytest` command.

Run all tests:
```bash
pytest tests/
```

Run tests with verbose output:
```bash
pytest -v tests/
```

Run tests and generate a coverage report:
```bash
pytest --cov=. tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[I Need to Specify our license here]
