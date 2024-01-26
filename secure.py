from cryptography.fernet import Fernet, InvalidToken
import os

# Generate or load the symmetric key for encryption
KEY_FILE = "encryption_key.key"
# Access the variables ENV
encryption_key = os.getenv("ENCRYPTION_KEY")
# print(f"READ ENCRYPTION_KEY: {encryption_key}")

def get_cipher_suite():
    try:
        Fernet(encryption_key) # Try to create a Fernet object to validate the key
    except (IOError, ValueError, InvalidToken) as e:
        print(f"Error: Unable to validate key please check !!'. {str(e)}")
    cipher_suite = Fernet(encryption_key)
    return cipher_suite

cipher_suite = get_cipher_suite()

def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

# # NOTE : RUN This before app execution IF NEEDED !!
# # USED TO HAVE CHECK BEFORE USER RUN APP
# # ON running app, we need to generate from key of create
# def check_key_or_take_key():
#     if os.path.exists(KEY_FILE):
#         print(f"The file '{KEY_FILE}' exists. I am using it")
#         return  

#     key = input("Enter your key (press enter to generate key) : ")
#     if key=="":
#         key = Fernet.generate_key()
#     else:
#         # Converting user entered key to bytes and storing it.
#         key = str.encode(key)

#     with open(KEY_FILE, "wb") as key_file:
#         key_file.write(key)
