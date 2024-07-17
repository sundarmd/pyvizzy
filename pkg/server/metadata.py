from flask import Flask, jsonify
import logging
from typing import Dict, Any

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_metadata_key

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

@app.route('/project/<project_id>/metadata', methods=['GET'])
def get_metadata(project_id: str):
    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400

    s3 = get_file_manager()

    try:
        metadata: Dict[str, Any] = s3.read_json(get_metadata_key(project_id))
    except Exception as e:
        logging.error(f"Error getting metadata from s3 for project {project_id}: {str(e)}")
        return jsonify({"error": "project metadata not found"}), 404

    return jsonify(metadata), 200

if __name__ == '__main__':
    app.run(debug=True)