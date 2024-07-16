import json
import os
from typing import Dict, Optional

from prompt import extract_code, extract_title  # Assuming these are implemented in a 'prompt' module

MAX_SAMPLE_LENGTH = 1000

class Visualization:
    def __init__(self, title: str, code: str):
        self.title = title
        self.code = code

class Engine:
    def query_with_template(self, template: str, data: Dict):
        # This method should be implemented according to your specific needs
        pass

    def create_visualization(self, user_request: str, desc: Dict, fields_metadata: Dict, sample: str, prev: Optional[Visualization] = None) -> Visualization:
        if len(sample) > MAX_SAMPLE_LENGTH:
            sample = sample[:MAX_SAMPLE_LENGTH]

        description_map = json.loads(json.dumps(desc))
        description_map["fieldsMetadata"] = fields_metadata
        description_map["sample"] = sample

        data = {
            "prompt": user_request,
            "data": description_map
        }

        do_plan = os.getenv("PLAN_IN_SEPARATE_QUERY") == "true"
        if do_plan and prev is None:
            plan = self.query_with_template("plan-visualization", data)
            data["plan"] = plan

        template = "create-visualization"
        if prev is not None:
            prev_map = json.loads(json.dumps(vars(prev)))
            data["current"] = prev_map
            template = "update-visualization"

        resp = self.query_with_template(template, data)

        code = extract_code(resp)
        title = extract_title(resp)

        if not title:
            title = prev.title if prev else "Untitled"

        return Visualization(title=title, code=code)