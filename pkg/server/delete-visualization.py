from flask import Flask, request, jsonify
import logging

# Assuming this module is implemented similarly to its Go counterpart
from files import get_file_manager

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

@app.route('/project/<project_id>/visualization/<visualization_id>', methods=['DELETE'])
def delete_visualization(project_id, visualization_id):
    if not project_id:
        return jsonify({"error": "Project ID is required"}), 400

    if not visualization_id:
        return jsonify({"error": "Visualization ID is required"}), 400

    s3 = get_file_manager()
    viz_key = f"projects/{project_id}/visualizations/{visualization_id}/"

    try:
        s3.delete_recursive(viz_key)
    except Exception as e:
        logging.error(f"Failed to delete visualization: {str(e)}")
        return jsonify({"error": str(e)}), 500

    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(debug=True)