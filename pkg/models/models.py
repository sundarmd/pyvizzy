from typing import Dict, List

class DataUpload:
    def __init__(self, uuid: str, key: str, raw_data: bytes):
        self.uuid = uuid
        self.key = key
        self.raw_data = raw_data

class Metadata:
    def __init__(self, format: str, title: str, description: str, fields: List[str]):
        self.format = format
        self.title = title
        self.description = description
        self.fields = fields

class VisualizationDetail:
    def __init__(self, prompt: str, code: str):
        self.prompt = prompt
        self.code = code

class Visualization:
    def __init__(self, uuid: str, details: str, visualizations: Dict[str, VisualizationDetail]):
        self.uuid = uuid
        self.details = details
        self.visualizations = visualizations