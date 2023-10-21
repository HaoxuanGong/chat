import ssl

SSL_KEY = "configs/cert.pem"
SSL_CERT = "configs/cert.pem"
CIPHER = 'AES128-SHA'


class EncryptionContext:

    def __init__(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(certfile=SSL_CERT, keyfile=SSL_KEY)
        self.context.load_verify_locations(SSL_CERT)
        self.context.set_ciphers(CIPHER)

    def wrap_socket(self, sock, server_side=True):
        return self.context.wrap_socket(sock, server_side=server_side)