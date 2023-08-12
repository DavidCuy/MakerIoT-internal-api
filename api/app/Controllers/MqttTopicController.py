from api.app.Core.Controllers.BaseController import index, find, store, update, delete
from api.app.Exceptions.APIException import APIException
from api.app.Validators.RequestValidator import RequestValidator
from api.database.DBConnection import AlchemyEncoder, AlchemyRelationEncoder, get_session
from api.app.Data.Enum.http_status_code import HTTPStatusCode
from api.utils.http_utils import build_response

import Environment as env
import os
from api.utils.cert_manager import CertManager
from api.utils.storage import Storage

import json
import logging
from flask import request

def generateCSR(certManager: CertManager, private_key: str, client_name: str):
    if not Storage('local', 'client-credentials').file_exist(f"{client_name}.csr"):
        csr_bytes = certManager.generate_certificate_signing_request(private_key, 'localhost', ['localhost', 'mosquitto', 'host.docker.internal'], ['127.0.0.1'])
        Storage('local', 'client-credentials').put(f"{client_name}.csr", csr_bytes)
    return Storage('local', 'client-credentials').get(f"{client_name}.csr").decode('utf-8')

def generatePrivateKey(certManager: CertManager, client_name: str):
    if not Storage('local', 'client-credentials').file_exist(f"{client_name}.key"):
        pkey = certManager.generate_private_key()
        Storage('local', 'client-credentials').put(f"{client_name}.key", pkey)
    return Storage('local', 'client-credentials').get(f"{client_name}.key").decode('utf-8')


def askCertSign(certManager: CertManager, ca_cert, ca_key, csr, client_name: str):
    if not Storage('local', 'client-credentials').file_exist(f"{client_name}.crt"):
        cert = certManager.generate_self_signed_certificate(ca_cert, ca_key, csr)
        Storage('local', 'client-credentials').put(f"{client_name}.crt", cert)
    return Storage('local', 'client-credentials').get(f"{client_name}.crt").decode('utf-8')

def generate_certificate(service):
    #TODO: implementar guardado en bd
    session = get_session()
    
    RequestValidator(session, { "client_name": ["required", "string"] }).validate()
    input_params = request.get_json()
    client_name = input_params["client_name"]
    
    certManager = CertManager()
    try:
        ca_cert = Storage('local', 'server-credentials').get(env.SERVER_CA_CERT).decode('utf-8')
        ca_key = Storage('local', 'server-credentials').get(env.SERVER_CA_KEY).decode('utf-8')
        key = generatePrivateKey(certManager, client_name)
        csr = generateCSR(certManager, key, client_name)
        cert = askCertSign(certManager, ca_cert, ca_key, csr, client_name)
        body = {
            "csr": csr,
            "key": key,
            "cert": cert
        }
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
