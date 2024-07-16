import json
from typing import Dict, Any

# Assuming prompt module is implemented similarly to the Go version
from prompt import extract_code

MAX_SAMPLE_LENGTH = 1000  # This value isn't defined in the Go script, so I'm using the value from a previous example

class DataDescription:
    # Assuming this class is defined as in the previous example
    pass

class Engine:
    def query_with_template(self, template: str, data: Dict[str, Any]) -> str:
        # This method should be implemented according to your specific needs
        pass

    def describe_fields(self, desc: DataDescription, sample: str) -> str:
        if len(sample) > MAX_SAMPLE_LENGTH:
            sample = sample[:MAX_SAMPLE_LENGTH]

        description_map = json.loads(json.dumps(vars(desc)))
        description_map["sample"] = sample

        data = {
            "data": description_map
        }

        resp = self.query_with_template("describe-fields", data)
        return extract_code(resp)