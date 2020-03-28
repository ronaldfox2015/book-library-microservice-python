
#/src/controllers/TodoController.py
from flask import request, g, Blueprint, json, Response
from .dto.response import DtoResponse
home_api = Blueprint('home_api', __name__)

@home_api.route('/health', methods=['GET'])
def health():
    return response({'health': True}, 200)

def response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )