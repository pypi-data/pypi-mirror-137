import hashlib
import base64

from Crypto import Random
from Crypto.Cipher import AES
    
BS = 16


def unpad(s): return s[0:-ord(s[-1:])]


def pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf8')


class HASH:

    def __init__(self):
        self.charset = 'utf-8'

    def hash(self, raw):
        return hashlib.sha256(raw.encode(self.charset)).hexdigest()


class AESCipher:

    def __init__(self, key, iv=None):
        self.charset = 'utf-8'
        self.key = key.encode(self.charset)
        self.iv = iv

    def encrypt(self, raw):
        raw = pad(raw.encode('utf8'))

        iv = Random.new().read(AES.block_size) if self.iv is None else self.iv
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16] if self.iv is None else self.iv
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode('utf8')

    def hash(self, raw):
        return hashlib.sha256(raw.encode(self.charset)).hexdigest()
