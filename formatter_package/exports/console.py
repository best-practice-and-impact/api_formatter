from typing import Any
from .base import BaseExporter


class ConsoleExportStrategy(BaseExporter):
    """
    Export data to the console.
    """
    def export(self, data: Any) -> None:
        """
        Export the given data to the console.
        """
        for key, value in data.items():
            print(f"{key}")
            if isinstance(value, list):
                for item in value:
                    for sub_key, sub_value in item.items():
                        print(f"  {sub_key}: {sub_value}")

                    print()
            else:
                print(f"  {value}")