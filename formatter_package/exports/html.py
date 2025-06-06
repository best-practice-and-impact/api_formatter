import json
from exports.base import BaseExporter

class HTMLExporter(BaseExporter):

    def export(self, filepath: str):
        data = json.dumps(self.serializer(), indent=4)
        html_content = f"""
        <html>
        <body>
            <h1>File Metadata</h1>
            <pre>{data}</pre>
        </body>
        </html>
        """
        with open(filepath, 'w') as f:
            f.write(html_content)
