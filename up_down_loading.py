from flask import request, make_response, send_file, jsonify
from flask import current_app as app
from werkzeug.utils import secure_filename
import os
import dbQueryManager
import json
import io
import zipfile
import time
import json
from flask import Blueprint

loading_api = Blueprint('loading_api', __name__, url_prefix="/load")

DB = dbQueryManager.dbQueryManager()
defaultCollection = "bagfiles_test"

@loading_api.route("/upload", methods=['GET', 'POST'])
def uploadBags():
    if request.method == 'POST':
        file = request.files['upload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            status = DB.addFile(defaultCollection, filename)
            if status:
                return make_response(jsonify({"status": "server"}), 200)
            else:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return make_response(jsonify({"status": "error"}), 200)

@loading_api.route("/download", methods=['GET'])
def downBags():
    uploaded = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        files = ["Double.bag", "hello.bag", "square.bag"]
        for individualFile in files:
            data = zipfile.ZipInfo(individualFile)
            data.date_time = time.localtime(time.time())[:6]
            data.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(data, os.path.join(uploaded, individualFile))
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename='capsule.zip', cache_timeout=0)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['bag'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS