import os, sys
sys.path.insert(0, os.path.abspath("./"))

import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint, make_response
from services.auth_service import token_required
from services.template_service import TemplateService

template_route = Blueprint('template_route', __name__)
templateService = TemplateService()

def get_blueprint():
    return template_route

@template_route.route('/template/<id>', methods=['GET'])
@token_required
def templateSingle(current_user, id):
    data = templateService.templateSingle(id)
    return make_response(jsonify(data), 200 if data["success"] else 403)

@template_route.route('/template', methods=['GET'])
@token_required
def templateAll(current_user):
    data = templateService.templateAll()
    return make_response(jsonify(data), 200 if data["success"] else 403)

@template_route.route('/template', methods=['POST'])
@token_required
def templateNew(current_user):
    data = templateService.templateNew(request.json)
    return make_response(jsonify(data), 201 if data["success"] else 403)

@template_route.route('/template/<id>', methods=['PUT'])
@token_required
def templateUpdate(current_user, id):
    data = templateService.templateUpdate(id, request.json)
    return make_response(jsonify(data), 201 if data["success"] else 403)

@template_route.route('/template/<id>', methods=['DELETE'])
@token_required
def templateDelete(current_user, id):
    data = templateService.templateDelete(id)
    return make_response(jsonify(data), 201 if data["success"] else 403)