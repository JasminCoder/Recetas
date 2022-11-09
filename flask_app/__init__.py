#__INIT__.PY

from flask import Flask

app = Flask(__name__)

app.secret_key = "llave secreta"

