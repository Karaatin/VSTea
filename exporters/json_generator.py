import json

class JSONExporter:
    def generate(self, plugins, output_path) -> bool:
        try:
            data = [p.to_dict() for p in plugins]

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            return True
        except Exception as e:
            return False