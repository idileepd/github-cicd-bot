from cryptography.fernet import Fernet

def generate_key(file_path="encryption_key.key"):
    key = Fernet.generate_key()
    with open(file_path, "wb") as key_file:
        key_file.write(key)
    return key

if __name__ == "__main__":
    key = generate_key()
    print(":::::Key Generated\n")
    print(key.decode())
    print("\n:::Saved to 'encryption_key.key'")
