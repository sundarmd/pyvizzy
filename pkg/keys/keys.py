import uuid
import os

def generate_uuid():
    return str(uuid.uuid4())

def get_email_key(email: str) -> str:
    return f"emails/{generate_uuid()}.txt"

def get_project_directory_key(project_id: str) -> str:
    return f"projects/{project_id}/"

def get_data_key(project_id: str) -> str:
    return f"{get_project_directory_key(project_id)}data"

def get_metadata_key(project_id: str) -> str:
    return f"{get_project_directory_key(project_id)}metadata.json"

def get_access_key_key(project_id: str) -> str:
    return f"{get_project_directory_key(project_id)}key.txt"

def get_fields_code_key(project_id: str) -> str:
    return f"{get_project_directory_key(project_id)}fields.json"

def get_visualization_directory_key(project_id: str, visualization_id: str) -> str:
    return f"{get_project_directory_key(project_id)}visualizations/{visualization_id}/"

def get_visualization_version_key(project_id: str, visualization_id: str, version: int) -> str:
    return f"{get_visualization_directory_key(project_id, visualization_id)}{version}.json"