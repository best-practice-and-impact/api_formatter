from exports.json import JSONExporter
from exports.yaml import YAMLExporter
from exports.html import HTMLExporter
from models.file_record import FileRecord

class ExportService:
    def export_json(self, record: FileRecord, filepath: str = None):
        exporter = JSONExporter(record)
        exporter.export(filepath)

    def export_yaml(self, record: FileRecord, filepath: str = None):
        exporter = YAMLExporter(record)
        exporter.export(filepath)

    def export_html(self, record: FileRecord, filepath: str):
        exporter = HTMLExporter(record)
        exporter.export(filepath)
