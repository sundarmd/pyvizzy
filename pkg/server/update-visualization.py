from flask import Flask, request, jsonify
import logging
from typing import Dict, Any

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_visualization_version_key, get_metadata_key, get_fields_code_key, get_data_key
from query import DataDescription, Visualization
from openai_client import get_openai_client

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

class UpdateVisualizationRequestBody:
    def __init__(self, code: str):
        self.code = code

@app.route('/project/<project_id>/visualization/<visualization_id>/version/<version_id>', methods=['PATCH'])
def update_visualization(project_id: str, visualization_id: str, version_id: str):
    s3 = get_file_manager()

    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400
    if not visualization_id:
        return jsonify({"error": "Visualization ID is required"}), 400
    if not version_id:
        return jsonify({"error": "Version ID is required"}), 400

    try:
        version_id = int(version_id)
    except ValueError:
        return jsonify({"error": "Version ID must be an integer"}), 400

    next_version_id = version_id + 1

    try:
        base_visualization = s3.read_json(get_visualization_version_key(project_id, visualization_id, version_id))
    except Exception as e:
        logging.error(f"Error getting current version from s3 for project {project_id}: {str(e)}")
        return jsonify({"error": "project visualization not found"}), 404

    prev = Visualization(
        title=base_visualization["title"],
        code=base_visualization["visualization"]
    )

    new_title = request.args.get('title') or base_visualization.get("title", "")
    new_code = ""
    prompt = ""

    if request.content_length:
        try:
            req_body = UpdateVisualizationRequestBody(**request.get_json())
            new_code = req_body.code
            prompt = "[manual edit]"
        except Exception as e:
            return jsonify({"error": "Invalid request body"}), 400

    if not new_code:
        prompt = request.args.get('prompt')
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        try:
            oai_client = get_openai_client(request)
        except Exception as e:
            logging.error(str(e))
            return jsonify({"error": str(e)}), 500

        try:
            metadata: DataDescription = s3.read_json(get_metadata_key(project_id))
        except Exception as e:
            logging.error(f"Error getting metadata from s3 for project {project_id}: {str(e)}")
            return jsonify({"error": "project metadata not found"}), 404

        try:
            fields_code: Dict[str, Any] = s3.read_json(get_fields_code_key(project_id))
            fields_metadata = fields_code.get("metadata", {})
        except Exception as e:
            logging.error(f"Error getting fields metadata from s3 for project {project_id}: {str(e)}")
            return jsonify({"error": "project fields metadata not found"}), 404

        try:
            data = s3.read_file(get_data_key(project_id))
        except Exception as e:
            logging.error(f"Error getting data from s3 for project {project_id}: {str(e)}")
            return jsonify({"error": "project data not found"}), 404

        try:
            viz = oai_client.create_visualization(prompt, metadata, fields_metadata, data.decode('utf-8'), prev)
            new_code = viz.code
            new_title = viz.title
        except Exception as e:
            logging.error(f"Error creating visualization for project {project_id}: {str(e)}")
            return jsonify({"error": "error creating visualization"}), 500

    data = {
        "id": visualization_id,
        "prompt": prompt,
        "visualization": new_code,
        "title": new_title,
    }

    try:
        s3.write_json(get_visualization_version_key(project_id, visualization_id, next_version_id), data)
    except Exception as e:
        logging.error(f"Error writing visualization to s3 for project {project_id}: {str(e)}")
        return jsonify({"error": "error creating visualization"}), 500

    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)