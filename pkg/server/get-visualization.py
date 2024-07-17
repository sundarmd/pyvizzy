from flask import Flask, jsonify, request
from typing import Dict, Any
import logging

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_visualization_version_key

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

@app.route('/project/<project_id>/visualization/<visualization_id>/version/<version>', methods=['GET'])
def get_visualization(project_id: str, visualization_id: str, version: str):
    try:
        version_int = int(version)
    except ValueError:
        return jsonify({"error": "version must be an integer"}), 400

    if not project_id or not visualization_id:
        return jsonify({"error": "you must specify a projectID, visualizationID, and version"}), 400

    s3 = get_file_manager()

    try:
        viz: Dict[str, Any] = s3.read_json(get_visualization_version_key(project_id, visualization_id, version_int))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(viz), 200

if __name__ == '__main__':
    app.run(debug=True)