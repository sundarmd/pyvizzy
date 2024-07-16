import json
from typing import List, Dict, Any
from dataclasses import dataclass

# Assuming prompt module is implemented similarly to the Go version
from prompt import extract_json_object

CHARS_TO_ANALYZE = 8000

@dataclass
class DataDescription:
    type: str = ""
    title: str = ""
    description: str = ""
    data_format: str = ""
    fields: List[str] = None
    suggested_visualizations: List[str] = None

    def __post_init__(self):
        if self.fields is None:
            self.fields = []
        if self.suggested_visualizations is None:
            self.suggested_visualizations = []

class Engine:
    def query_with_template(self, template: str, data: Dict[str, Any]) -> str:
        # This method should be implemented according to your specific needs
        pass

    def describe_data(self, data: str) -> DataDescription:
        data = data[:min(CHARS_TO_ANALYZE, len(data))]

        resp = self.query_with_template("describe-data", {"data": data, "characters": CHARS_TO_ANALYZE})

        desc = parse_json_object(resp, DataDescription)
        return desc

def parse_json_object(body: str, cls: Any) -> Any:
    json_object = extract_json_object(body)
    return cls(**json.loads(json_object))

def min(a: int, b: int) -> int:
    return a if a < b else b