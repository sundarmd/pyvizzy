from flask import Flask, request, jsonify
import logging

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_visualization_version_key

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/project/<project_id>/visualization/<visualization_id>/version/<version_id>', methods=['DELETE'])
def delete_visualization_version(project_id, visualization_id, version_id):
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

    logging.info(f"Deleting visualization version {version_id} for project {project_id}")

    try:
        s3.delete_file(get_visualization_version_key(project_id, visualization_id, version_id))
    except Exception as e:
        logging.error(f"Error deleting visualization version from s3 for project {project_id}: {str(e)}")
        return jsonify({"error": "Error deleting visualization version"}), 500

    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(debug=True)