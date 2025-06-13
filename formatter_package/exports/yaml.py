import yaml
from rich import print as rprint
from rich.syntax import Syntax
from exports.base import BaseExporter

class YAMLExporter(BaseExporter):

    def export(self, filepath: str = None):
        data = yaml.dump(self.serializer(), sort_keys=False)
        if filepath:
            with open(filepath, 'w') as f:
                f.write(data)
        else:
            rprint(Syntax(data, "yaml", theme="monokai", line_numbers=True))
