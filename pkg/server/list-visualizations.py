from flask import Flask, jsonify
import logging

# Assuming this module is implemented similarly to its Go counterpart
from files import get_file_manager

app = Flask(__name__)
logging.basicConfig(level=logging.WARNING)

@app.route('/project/<project_id>/visualizations', methods=['GET'])
def list_visualizations(project_id):
    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400

    s3 = get_file_manager()
    project_key = f"projects/{project_id}/visualizations/"

    try:
        files = s3.list_directories(project_key)
    except Exception as e:
        logging.warning(f"Failed to list files, assuming empty: {str(e)}")
        files = []

    return jsonify({"ids": files}), 200

if __name__ == '__main__':
    app.run(debug=True)