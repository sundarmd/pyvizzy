import os
from flask import Flask, send_from_directory, abort, request
from werkzeug.middleware.proxy_fix import ProxyFix

# Assuming these functions are implemented in separate modules
from api_handlers import (
    upload_data, save_email, get_metadata, list_visualizations, get_data,
    get_fields_code, fork_project, get_visualization, get_latest_visualization,
    list_versions, set_metadata, analyze_data, create_visualization,
    describe_fields, set_fields_metadata, delete_project, delete_visualization,
    update_visualization, delete_visualization_version
)
from middleware import check_key

app = Flask(__name__, static_folder='./app/dist')
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path.startswith('api'):
        abort(404)
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# API routes
@app.route('/api/projects', methods=['POST'])
def api_upload_data():
    return upload_data()

@app.route('/api/email', methods=['POST'])
def api_save_email():
    return save_email()

# Project view routes
@app.route('/api/projects/<project_id>/metadata', methods=['GET'])
def api_get_metadata(project_id):
    return get_metadata(project_id)

@app.route('/api/projects/<project_id>/visualizations', methods=['GET'])
def api_list_visualizations(project_id):
    return list_visualizations(project_id)

@app.route('/api/projects/<project_id>/data', methods=['GET'])
def api_get_data(project_id):
    return get_data(project_id)

@app.route('/api/projects/<project_id>/fields-code', methods=['GET'])
def api_get_fields_code(project_id):
    return get_fields_code(project_id)

@app.route('/api/projects/<project_id>/fork', methods=['POST'])
def api_fork_project(project_id):
    return fork_project(project_id)

# Visualization view routes
@app.route('/api/projects/<project_id>/visualizations/<visualization_id>/versions/<version>', methods=['GET'])
def api_get_visualization(project_id, visualization_id, version):
    return get_visualization(project_id, visualization_id, version)

@app.route('/api/projects/<project_id>/visualizations/<visualization_id>/latest', methods=['GET'])
def api_get_latest_visualization(project_id, visualization_id):
    return get_latest_visualization(project_id, visualization_id)

@app.route('/api/projects/<project_id>/visualizations/<visualization_id>/versions', methods=['GET'])
def api_list_versions(project_id, visualization_id):
    return list_versions(project_id, visualization_id)

# Project edit routes (with authentication)
@app.route('/api/projects/<project_id>/metadata', methods=['POST'])
@check_key
def api_set_metadata(project_id):
    return set_metadata(project_id)

@app.route('/api/projects/<project_id>/analyze', methods=['POST'])
@check_key
def api_analyze_data(project_id):
    return analyze_data(project_id)

@app.route('/api/projects/<project_id>/visualizations', methods=['POST'])
@check_key
def api_create_visualization(project_id):
    return create_visualization(project_id)

@app.route('/api/projects/<project_id>/fields-code', methods=['POST'])
@check_key
def api_describe_fields(project_id):
    return describe_fields(project_id)

@app.route('/api/projects/<project_id>/fields-metadata', methods=['POST'])
@check_key
def api_set_fields_metadata(project_id):
    return set_fields_metadata(project_id)

@app.route('/api/projects/<project_id>', methods=['DELETE'])
@check_key
def api_delete_project(project_id):
    return delete_project(project_id)

# Visualization edit routes (with authentication)
@app.route('/api/projects/<project_id>/visualizations/<visualization_id>', methods=['DELETE'])
@check_key
def api_delete_visualization(project_id, visualization_id):
    return delete_visualization(project_id, visualization_id)

@app.route('/api/projects/<project_id>/visualizations/<visualization_id>/versions/<version_id>', methods=['PATCH'])
@check_key
def api_update_visualization(project_id, visualization_id, version_id):
    return update_visualization(project_id, visualization_id, version_id)

@app.route('/api/projects/<project_id>/visualizations/<visualization_id>/versions/<version_id>', methods=['DELETE'])
@check_key
def api_delete_visualization_version(project_id, visualization_id, version_id):
    return delete_visualization_version(project_id, visualization_id, version_id)

if __name__ == '__main__':
    port = os.getenv('PORT', '3031')
    app.run(host='0.0.0.0', port=int(port))

    #pip install flask werkzeug