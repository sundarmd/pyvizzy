from flask import Flask, request, jsonify
import logging

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_project_directory_key

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

@app.route('/project/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400

    s3 = get_file_manager()
    try:
        s3.delete_recursive(get_project_directory_key(project_id))
    except Exception as e:
        logging.error(f"Failed to delete project: {str(e)}")
        return jsonify({"error": str(e)}), 500

    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(debug=True)