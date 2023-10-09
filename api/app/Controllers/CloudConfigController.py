from api.app.Core.Controllers.BaseController import index, find, delete
import json
from typing import cast
from flask import request
import logging
from api.app.Data.Enum.http_status_code import HTTPStatusCode

from api.app.Exceptions.APIException import APIException
from api.app.Validators.RequestValidator import RequestValidator

from api.app.Data.Interfaces.PaginationResult import PaginationResult
from api.app.Data.Models import CloudConfig
from api.app.Services import CloudConfigService
from api.database.DBConnection import AlchemyEncoder, AlchemyRelationEncoder, get_session
from api.utils.http_utils import build_response, get_paginate_params, get_filter_params, get_relationship_params, get_search_method_param, get_search_params
from api.utils.storage import Storage

SUCCESS_STATUS = 200
UNAUTHORIZED_STATUS = 401
ERROR_STATUS = 400

service: CloudConfigService = CloudConfigService()

def store():
    session = get_session()
    
    RequestValidator(session, service.get_rules_for_store()).validate()
    RequestValidator(session, {"provider": ["required", "string"]}).validate()

    input_params = request.get_json()
    RequestValidator(session, service.update_rules_store_from_provider(input_params['provider'])).validate()

    try:
        del input_params['provider']
        body = service.insert_register(session, input_params)
        response = json.dumps(body, cls=AlchemyEncoder)
        status_code = HTTPStatusCode.OK.value
    except APIException as e:
        logging.exception("APIException occurred")
        response = json.dumps(e.to_dict())
        status_code = e.status_code
    except Exception:
        logging.exception("No se pudo realizar la consulta")
        body = dict(message="No se pudo realizar la consulta")
        response = json.dumps(body)
        status_code=HTTPStatusCode.UNPROCESABLE_ENTITY.value
    finally:
        session.close()
    
    return build_response(status_code, response, is_body_str=True)

