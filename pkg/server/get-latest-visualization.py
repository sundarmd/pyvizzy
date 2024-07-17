from flask import Flask, jsonify, request
import logging
from typing import Dict, Any
import os

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_visualization_version_key

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/project/<project_id>/visualization/<visualization_id>/latest', methods=['GET'])
def get_latest_visualization(project_id: str, visualization_id: str):
    if not project_id or not visualization_id:
        return jsonify({"error": "you must specify a projectID and visualizationID"}), 400

    s3 = get_file_manager()
    viz_key = f"projects/{project_id}/visualizations/{visualization_id}/"

    try:
        versions = s3.list_files_recursive(viz_key)
    except Exception as e:
        logging.error(f"Error listing versions: {str(e)}")
        return jsonify({"error": str(e)}), 400

    logging.info(f"Found {len(versions)} versions for {viz_key}")
    
    largest = 0
    for ver in versions:
        logging.info(ver)
        parts = ver.split('/')
        if not parts:
            logging.warning(f"invalid version {ver}")
            continue
        ver = os.path.splitext(parts[-1])[0]
        try:
            ver_num = int(ver)
        except ValueError:
            logging.warning(f"invalid version parse {ver}")
            continue
        largest = max(largest, ver_num)

    try:
        viz: Dict[str, Any] = s3.read_json(get_visualization_version_key(project_id, visualization_id, largest))
    except Exception as e:
        logging.error(f"Error reading visualization: {str(e)}")
        return jsonify({"error": str(e)}), 400

    viz["version"] = largest
    return jsonify(viz), 200

if __name__ == '__main__':
    app.run(debug=True)