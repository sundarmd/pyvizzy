from flask import Flask, request, jsonify
import logging
import requests
from io import BytesIO
from typing import Union, Tuple

# Assuming these modules are implemented similarly to their Go counterparts
from files import get_file_manager
from keys import generate_uuid, get_data_key, get_access_key_key

app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
MAX_FILE_SIZE_STRING = "100MB"

def read_limited_stream(stream: Union[BytesIO, requests.Response], max_size: int) -> Tuple[bytes, bool]:
    data = b''
    for chunk in stream.iter_content(chunk_size=8192):
        data += chunk
        if len(data) > max_size:
            return data[:max_size], True
    return data, False

@app.route('/upload', methods=['POST'])
def upload_data():
    s3 = get_file_manager()

    url = request.args.get('url')
    if url:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            data_stream = response
            data_length = int(response.headers.get('Content-Length', 0))
        except requests.RequestException as e:
            return jsonify({"error": f"Invalid URL: {str(e)}"}), 400
    else:
        data_stream = BytesIO(request.data)
        data_length = request.content_length or 0

    if data_length > MAX_FILE_SIZE:
        return jsonify({"error": f"File size exceeds {MAX_FILE_SIZE_STRING}"}), 413

    raw_data, exceeded = read_limited_stream(data_stream, MAX_FILE_SIZE)
    if exceeded:
        return jsonify({"error": f"Invalid data or data size too large"}), 413

    project_id = generate_uuid()

    try:
        s3.write_file(get_data_key(project_id), raw_data)
    except Exception as e:
        logging.error(f"Failed to upload data: {str(e)}")
        return jsonify({"error": "Failed to upload data"}), 500

    auth_key = generate_uuid()
    try:
        s3.write_file(get_access_key_key(project_id), auth_key.encode('utf-8'))
    except Exception as e:
        logging.error(f"Failed to upload authentication key: {str(e)}")
        return jsonify({"error": "Failed to upload authentication key"}), 500

    return jsonify({"uuid": project_id, "key": auth_key}), 200

if __name__ == '__main__':
    app.run(debug=True)