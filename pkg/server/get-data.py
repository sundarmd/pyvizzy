from flask import Flask, request, jsonify, Response
import logging

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_data_key

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

@app.route('/project/<project_id>/data', methods=['GET'])
def get_data(project_id):
    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400

    s3 = get_file_manager()

    try:
        data = s3.read_file(get_data_key(project_id))
    except Exception as e:
        logging.error(f"Error getting data from s3 for project {project_id}: {str(e)}")
        return jsonify({"error": "project data not found"}), 404

    return Response(data, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)