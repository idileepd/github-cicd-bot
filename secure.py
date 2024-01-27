from cryptography.fernet import Fernet, InvalidToken
import os

class Secure:
    _instance = None
    def __new__(cls):
        if cls._instance is None:

            # Create Singleton instance
            cls._instance = super(Secure, cls).__new__(cls)
            encryption_key = os.getenv("ENCRYPTION_KEY")
            try:
                cipher_suite = Fernet(encryption_key)
                cls._instance.cipher_suite = cipher_suite
            except Exception as e:
                print(f"Error: Unable to validate key please check !!")
                return

    @staticmethod
    def encrypt(plain_data):
        encrypted_data = Secure._instance.cipher_suite.encrypt(plain_data.encode())
        return encrypted_data
    
    @staticmethod
    def decrypt(encrypted_data):
        decrypted_data = Secure._instance.cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data

# initialize the singleton instance
Secure()
