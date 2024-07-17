from flask import Flask, jsonify
from typing import Dict, Any
import logging

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_fields_code_key

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

@app.route('/project/<project_id>/fields-code', methods=['GET'])
def get_fields_code(project_id: str):
    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400

    s3 = get_file_manager()

    try:
        code: Dict[str, Any] = s3.read_json(get_fields_code_key(project_id))
    except Exception as e:
        logging.error(f"Error reading fields code for project {project_id}: {str(e)}")
        return jsonify({"error": "fields code not found"}), 404

    return jsonify(code), 200

if __name__ == '__main__':
    app.run(debug=True)