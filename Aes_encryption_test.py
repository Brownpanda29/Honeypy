import hashlib
import base64
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt_data(encrypted_data, password):
    # Generate the decryption key from the password
    hashed_password = hashlib.sha256(password.encode()).digest()
    key = hashed_password[:32]

    # Create a new AES-256-CBC cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(b'\0' * 16), backend=default_backend())

    # Decrypt the encrypted data
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Remove the padding from the decrypted data
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return decrypted_data

def main():
    encrypted_data = bytes.fromhex(
        "9f86d081884c7d659a2feaa0c55ad023"
        "4a44dc15364204a80e9348c1239a2f01"
        "7f4a2b15689d30a22b0a1a9a8a9a2f0"
        "3a107b2a109a2a9a8a2f0a1a9a8a2f"
        "a22b0a1a9a8a2f0a1a9a8a2f0a1a9"
        "9a8a2f0a1a9a8a2f0a1a9a8a2f0a1"
        "2f0a1a9a8a2f0a1a9a8a2f0a1a9a8"
        "a1a9a8a2f0a1a9a8a2f0a1a9a8a2"
        "8a2f0a1a9a8a2f0a1a9a8a2f0a1a9"
        "2f0a1a9a8a2f0a1a9a8a2f0a1a9a8"
        "a9a8a2f0a1a9a8a2f0a1a9a8a2f0"
        "1a9a8a2f0a1a9a8a2f0a1a9a8a2f0"
        "8a2f0a1a9a8a2f0a1a9a8a2f0a1a9"
        "a1a9a8a2f0a1a9a8a2f0a1a9a8a2"
        "2f0a1a9a8a2f0a1a9a8a2f0a1a9a8"
        "9a8a2f0a1a9a8a2f0a1a9a8a2f0a1"
    )

    password = input("Enter the password: ")

    try:
        decrypted_data = decrypt_data(encrypted_data, password)
        print("Decrypted data:", decrypted_data.decode())
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
  
