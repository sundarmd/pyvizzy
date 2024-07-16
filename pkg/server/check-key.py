from flask import Flask, request, jsonify, abort
from functools import wraps
import logging

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import get_access_key_key

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

def check_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        project_id = kwargs.get('project_id')
        key_provided = request.headers.get('X-PROJECT-KEY')
        s3 = get_file_manager()

        try:
            actual_key = s3.read_file(get_access_key_key(project_id))
        except Exception as e:
            logging.error(f"Error reading key file: {str(e)}")
            return jsonify({"error": "project not found"}), 404

        if key_provided != actual_key.decode('utf-8'):
            return jsonify({"error": "unauthorized"}), 401

        return f(*args, **kwargs)
    return decorated_function

@app.route('/project/<project_id>', methods=['GET'])
@check_key
def project_route(project_id):
    # Your route logic here
    return jsonify({"message": "Project accessed successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)