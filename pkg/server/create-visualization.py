from flask import Flask, request, jsonify
import logging
from typing import Dict, Any

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_metadata_key, get_fields_code_key, get_data_key, get_visualization_version_key, generate_uuid
from query import DataDescription

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

def get_openai_client(request):
    # This function should be implemented based on your authentication mechanism
    pass

@app.route('/project/<project_id>/visualization', methods=['POST'])
def create_visualization(project_id: str):
    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400
    
    prompt = request.args.get('prompt')
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        oai_client = get_openai_client(request)
    except Exception as e:
        logging.error(str(e))
        return jsonify({"error": str(e)}), 500

    s3 = get_file_manager()

    try:
        metadata: DataDescription = s3.read_json(get_metadata_key(project_id))
    except Exception as e:
        logging.error(f"Error getting metadata from s3 for project {project_id}: {str(e)}")
        return jsonify({"error": "project metadata not found"}), 404

    try:
        fields_code: Dict[str, Any] = s3.read_json(get_fields_code_key(project_id))
    except Exception as e:
        logging.error(f"Error getting fields metadata from s3 for project {project_id}: {str(e)}")
        return jsonify({"error": "project fields metadata not found"}), 404

    fields_metadata = fields_code.get('metadata', {})

    try:
        data = s3.read_file(get_data_key(project_id))
    except Exception as e:
        logging.error(f"Error getting data from s3 for project {project_id}: {str(e)}")
        return jsonify({"error": "project data not found"}), 404

    viz_uuid = generate_uuid()
    try:
        viz = oai_client.create_visualization(prompt, metadata, fields_metadata, data.decode('utf-8'), None)
    except Exception as e:
        logging.error(f"Error creating visualization for project {project_id}: {str(e)}")
        return jsonify({"error": "error creating visualization"}), 500

    resp = {
        "id": viz_uuid,
        "prompt": prompt,
        "visualization": viz.code,
        "title": viz.title,
    }

    try:
        s3.write_json(get_visualization_version_key(project_id, viz_uuid, 1), resp)
    except Exception as e:
        logging.error(f"Error writing visualization to s3 for project {project_id}: {str(e)}")
        return jsonify({"error": "error creating visualization"}), 500

    return jsonify(resp), 200

if __name__ == '__main__':
    app.run(debug=True)