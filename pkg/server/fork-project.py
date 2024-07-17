from flask import Flask, request, jsonify
import logging
from typing import Dict, Any

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import generate_uuid, get_metadata_key, get_project_directory_key, get_access_key_key

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/project/<source_project_id>/fork', methods=['POST'])
def fork_project(source_project_id: str):
    s3 = get_file_manager()
    new_project_id = generate_uuid()
    logging.info(f"Forking project {source_project_id} to {new_project_id}")

    try:
        metadata: Dict[str, Any] = s3.read_json(get_metadata_key(source_project_id))
    except Exception as e:
        logging.error(f"Error getting metadata from s3 for project {source_project_id}: {str(e)}")
        return jsonify({"error": "project metadata not found"}), 404

    try:
        s3.copy_directory(
            get_project_directory_key(source_project_id), 
            get_project_directory_key(new_project_id)
        )
    except Exception as e:
        logging.error(f"Failed to copy project: {str(e)}")
        return jsonify({"error": "Failed to copy project"}), 500

    auth_key = generate_uuid()
    try:
        s3.write_file(get_access_key_key(new_project_id), auth_key.encode('utf-8'))
    except Exception as e:
        logging.error(f"Failed to generate authentication key: {str(e)}")
        return jsonify({"error": "Failed to generate authentication key"}), 500

    return jsonify({"uuid": new_project_id, "key": auth_key}), 200

if __name__ == '__main__':
    app.run(debug=True)