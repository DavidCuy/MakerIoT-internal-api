import random
from typing import Tuple
from OpenSSL import crypto

class CertManager:
    def __init__(self) -> None:
        pass
    
    def generate_cert_authority(self, CAName: str, country_code: str = 'MX', state: str = 'Tabasco', location: str = 'Emiliano Zapata',
                                organization: str = 'ChilliTech', organization_unit: str = 'Innovation',
                                expire_years: int = 5, bitlens: int = 2048, passlen: int = 64, digest: str = "sha512") -> Tuple[bytes, bytes]:
        seconds_in_years = int(expire_years * 3600 * 24 * 365.4)
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, bitlens)
        serialnumber = random.getrandbits(passlen)
        
        cert = crypto.X509()
        cert.get_subject().C = country_code
        cert.get_subject().ST = state
        cert.get_subject().L = location
        cert.get_subject().O = organization
        cert.get_subject().OU = organization_unit
        cert.get_subject().CN = CAName
        
        cert.set_serial_number(serialnumber)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(seconds_in_years)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)

        
        cert.sign(k, digest)
        pub=crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
        priv=crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
        
        return pub, priv
    
    def generate_private_key(self, bitLen: int = 2048):
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, bitLen)
        return crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
    
    def generate_certificate_signing_request(self, pkey: str, domain: str, dnsname=[], ipaddr=[], country_code: str = 'MX', state: str = 'Tabasco', location: str = 'Emiliano Zapata',
                                organization: str = 'ChilliTech', organization_unit: str = 'Innovation', digest: str = "sha256") -> bytes:
        
        ss = []
        for i in dnsname:
            ss.append("DNS: %s" % i)
        for i in ipaddr:
            ss.append("IP: %s" % i)
        ss = ", ".join(ss)

        # Add in extensions
        base_constraints = ([
            crypto.X509Extension(
                        b"keyUsage",
                        False,
                        b"Digital Signature, Non Repudiation, Key Encipherment"),
            crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
        ])
        x509_extensions = base_constraints
        
        key = crypto.load_privatekey(crypto.FILETYPE_PEM, pkey)
        req = crypto.X509Req()
        req.get_subject().CN = domain
        
        if ss:
            san_constraint = crypto.X509Extension(b"subjectAltName", False, ss.encode('utf-8'))
            x509_extensions.append(san_constraint)

        req.add_extensions(x509_extensions)

        
        req.get_subject().C = country_code
        req.get_subject().ST = state
        req.get_subject().L = location
        req.get_subject().O = organization
        req.get_subject().OU = organization_unit
        req.set_pubkey(key)
        req.sign(key, digest)
        
        return crypto.dump_certificate_request(crypto.FILETYPE_PEM, req)
    
    def generate_self_signed_certificate(self, ca_cert: str, ca_key: str, csr_str: str, passlen:int = 64, offset_valid_seconds: int = 0, expire_years: int = 1, digest: str = "sha256") -> bytes:
        ca = crypto.load_certificate(crypto.FILETYPE_PEM, ca_cert)
        key = crypto.load_privatekey(crypto.FILETYPE_PEM, ca_key)
        csr = crypto.load_certificate_request(crypto.FILETYPE_PEM, csr_str)
        
        serialnumber = random.getrandbits(passlen)
        seconds_in_years = int(expire_years * 3600 * 24 * 365.4)
        
        cert = crypto.X509()
        cert.set_subject(csr.get_subject())
        cert.set_serial_number(serialnumber)
        cert.gmtime_adj_notBefore(offset_valid_seconds)
        cert.gmtime_adj_notAfter(seconds_in_years)
        cert.set_issuer(ca.get_subject())
        cert.set_pubkey(csr.get_pubkey())
        cert.sign(key, digest)
        
        return crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
