import uuid
from sys import version_info
from flask import Flask, request
from utils import get_conf
from waitress import serve

conf_dict = get_conf('conf/main.toml')['getcha']
# allowed extension name
ALLOWED_EXTENSIONS = set(conf_dict['allowed_extension'])
# where to store img file.
UPLOADED_FILEPATH = conf_dict['uploaded_filepath']

app = Flask(__name__)


def make_picture(path_file, data):
    filename = '\{}.png'.format(uuid.uuid4())
    with open(path_file + filename, 'wb') as f:
        f.write(data)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/images', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            data = file.stream.read()
            make_picture(UPLOADED_FILEPATH, data)
            return 'stored'
    return 'no'


if version_info[0] == 2:
    host, port = conf_dict['listen'].split(':')
    serve(app, host=host, port=port)


else:
    serve(app, listen=conf_dict['listen'])
