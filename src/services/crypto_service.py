from dependency_injector.wiring import Provide, inject
from passlib.context import CryptContext
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
import base64
from log2mongo import log2mongo

class CryptoService:
    
    #@inject
    def __init__(self, log: log2mongo) -> None:
        self.private_key = self.get_private_key()
        self.public_key = self.get_public_key()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.log = log
    
    async def get_psw_hash(self, password: str):
        return self.pwd_context.hash(password)
    
    async def verify_password(self, plain_pwd: str, hashed_psw: str):
        return self.pwd_context.verify(plain_pwd, hashed_psw)

    def get_private_key(self):
        try:
            print(f"read private key ")

            # private_key = rsa.generate_private_key(
            #     public_exponent=,
            #     key_size=4096,
            #     backend=default_backend()
            # )
            # public_key = private_key.public_key()
        
            # private_pem = private_key.private_bytes(
            #     encoding=serialization.Encoding.PEM,
            #     format=serialization.PrivateFormat.PKCS8,
            #     encryption_algorithm=serialization.NoEncryption()
            # )
        
            # with open('private_key.pem', 'wb') as f:
            #     f.write(private_pem)
            
            #     public_pem = public_key.public_bytes(
            #         encoding=serialization.Encoding.PEM,
            #         format=serialization.PublicFormat.SubjectPublicKeyInfo
            #         )
            
            # with open('public_key.pem', 'wb') as f:
            #     f.write(public_pem)
        
            with open("private_key.pem", "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
            return private_key
        
        except FileNotFoundError as e:
            self.log.logger.error(e)
            print("Error: private_key.pem not found.")
        except ValueError as e:
            self.log.logger.error(e)
            print(f"Error loading private key: {e}")

    def get_public_key(self):
        try:
            print(f"read public key ")
            
            with open("public_key.pem", "rb") as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(),
                    backend=default_backend()
                )
            return public_key
        
        except FileNotFoundError as e:
            self.log.logger.error(e)
            print("Error: private_key.pem not found.")
        except Exception as e:
            self.log.logger.error(e)
            print(f"Error loading private key: {e}")

    async def encrypt_text(self, text: str):
        try:
            public_key = self.public_key
            if public_key is not None:
                ciphertext = public_key.encrypt( # type: ignore
                    text.encode(),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                r = base64.b64encode(ciphertext)
                return str(r, "utf8" )
        except Exception as e:
            self.log.logger.error(e)
            raise e
    
    async def decrypt_text(self, text: str):
        try:
            private_key = self.private_key
            plaintext = private_key.decrypt( # type: ignore
                base64.b64decode(text),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                    )
                )
            return str(plaintext, "utf8")
        except Exception as e:
            self.log.logger.error(e)
            raise e