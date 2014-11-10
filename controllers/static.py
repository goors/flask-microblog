from flask import Blueprint

static_api = Blueprint('static_api', __name__)

@static_api.route('/about', methods=['GET'])
def legal():
    return False