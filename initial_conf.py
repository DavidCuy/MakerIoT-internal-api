#!/usr/bin/python
# this script makes the initial configuration to use TLS with mosquitto
# it generates the mosquitto key pair
# and retrieves a certificate and CRL from CA
# if the configuration has already been done before, this script does nothing

import Environment as env
from api.utils.cert_manager import CertManager
from api.utils.storage import Storage

def generateCertAuthority(certManager: CertManager):
    if not Storage('local', 'server-credentials').file_exist(env.SERVER_CA_CERT) or not Storage('local', 'server-credentials').file_exist(env.SERVER_CA_KEY) :
        cert_bytes, key_bytes = certManager.generate_cert_authority("mosquitto")
        
        Storage('local', 'server-credentials').put(env.SERVER_CA_CERT, cert_bytes)
        Storage('local', 'server-credentials').put(env.SERVER_CA_KEY, key_bytes)
    return Storage('local', 'server-credentials').get(env.SERVER_CA_CERT).decode('utf-8'), Storage('local', 'server-credentials').get(env.SERVER_CA_KEY).decode('utf-8')


def generateCSR(certManager: CertManager, private_key: str):
    if not Storage('local', 'server-credentials').file_exist(env.SERVER_CSR):
        csr_bytes = certManager.generate_certificate_signing_request(private_key, "localhost", ['localhost', 'mosquitto', 'host.docker.internal'], ['127.0.0.1'])
        Storage('local', 'server-credentials').put(env.SERVER_CSR, csr_bytes)
    return Storage('local', 'server-credentials').get(env.SERVER_CSR).decode('utf-8')

def generatePrivateKey(certManager: CertManager, save: bool = True):
    if not Storage('local', 'server-credentials').file_exist(env.SERVER_PRIVATE_KEY):
        pkey = certManager.generate_private_key()
        Storage('local', 'server-credentials').put(env.SERVER_PRIVATE_KEY, pkey)
    return Storage('local', 'server-credentials').get(env.SERVER_PRIVATE_KEY).decode('utf-8')


def askCertSign(certManager: CertManager, ca_cert, ca_key, csr, save: bool = True):
    if not Storage('local', 'server-credentials').file_exist(env.SERVER_CERT):
        cert = certManager.generate_self_signed_certificate(ca_cert, ca_key, csr)
        Storage('local', 'server-credentials').put(env.SERVER_CERT, cert)
    return Storage('local', 'server-credentials').get(env.SERVER_CERT).decode('utf-8')

def generate_server_credentials():
    certManager = CertManager()
    try:
        ca_cert, ca_key = generateCertAuthority(certManager)
        key = generatePrivateKey(certManager)
        csr = generateCSR(certManager, key)
        cert = askCertSign(certManager, ca_cert, ca_key, csr)
        print(cert)
    except Exception as e:
        print(str(e))
