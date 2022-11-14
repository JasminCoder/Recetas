#__INIT__.PY

from flask import Flask

app = Flask(__name__)

app.secret_key = "llave secreta"

app.config['UPLOAD_FOLDER'] = 'flask_app/static/img'