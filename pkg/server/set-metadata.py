from flask import Flask, request, jsonify
import logging
from typing import Dict, Any

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_metadata_key
from query import DataDescription

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

@app.route('/project/<project_id>/metadata', methods=['POST'])
def set_metadata(project_id: str):
    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400

    try:
        body_data = DataDescription(**request.get_json())
    except Exception as e:
        logging.error(f"Error parsing metadata JSON for project {project_id}: {str(e)}")
        return jsonify({"error": "error parsing metadata request body"}), 400

    s3 = get_file_manager()

    try:
        s3.write_json(get_metadata_key(project_id), body_data.__dict__)
    except Exception as e:
        logging.error(f"Error writing metadata to s3 for project {project_id}: {str(e)}")
        return jsonify({"error": "error writing project metadata"}), 500

    return jsonify(body_data.__dict__), 200

if __name__ == '__main__':
    app.run(debug=True)