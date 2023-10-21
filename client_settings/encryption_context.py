import ssl

CIPHER_SET = 'AES128-SHA'


class EncryptionContext:

    def __init__(self):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.set_ciphers(CIPHER_SET)

    def wrap_socket(self, sock, hostname):
        return self.context.wrap_socket(sock, server_hostname=hostname)

