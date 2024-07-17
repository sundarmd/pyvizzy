from flask import Flask, request, jsonify
import logging
from typing import Dict, Any

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_fields_code_key

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

@app.route('/project/<project_id>/fields-metadata', methods=['POST'])
def set_fields_metadata(project_id: str):
    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400

    s3 = get_file_manager()

    try:
        fields_data: Dict[str, Any] = s3.read_json(get_fields_code_key(project_id))
    except Exception as e:
        logging.error(f"Error reading fields code from s3 for project {project_id}: {str(e)}")
        return jsonify({"error": "error retrieving fields code"}), 500

    try:
        body_data: Dict[str, Any] = request.get_json()
    except Exception as e:
        logging.error(f"Error parsing JSON for project {project_id}: {str(e)}")
        return jsonify({"error": "error parsing request body"}), 400

    fields_data["metadata"] = body_data

    try:
        s3.write_json(get_fields_code_key(project_id), fields_data)
    except Exception as e:
        logging.error(f"Error writing fields code to s3 for project {project_id}: {str(e)}")
        return jsonify({"error": "error writing fields metadata"}), 500

    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(debug=True)