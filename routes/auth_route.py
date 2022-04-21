import os, sys
sys.path.insert(0, os.path.abspath("../services"))

from flask import jsonify, abort, request, Blueprint, make_response
from services.auth_service import AuthService

auth_route = Blueprint('auth_route', __name__)

authService = AuthService()

def get_blueprint():
    return auth_route


@auth_route.route('/register', methods=['POST'])
def register():
    regResp = authService.register(request.json)
    return make_response(jsonify(regResp), 201 if regResp["success"] else 403)

@auth_route.route('/login', methods=['POST'])
def login():
    loginResp = authService.login(request.json["email"], request.json["password"])
    return make_response(jsonify(loginResp), 201 if loginResp["success"] else 403)