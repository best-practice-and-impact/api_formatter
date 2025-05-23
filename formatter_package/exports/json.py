import json

from exports.base import BaseExporter


class JSONExporter(BaseExporter):

    def export(self, filepath: str = None):
        json_string = json.dumps(self.serializer(), indent=4)

        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_string)
        else:
            from rich import print as rprint
            from rich.syntax import Syntax
            rprint(Syntax(json_string, "json", theme="monokai", line_numbers=True))
