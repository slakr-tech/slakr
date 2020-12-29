from cryptography.fernet import Fernet
import os, sys

encryption_key = os.environ.get('chatreEncryptionKey')

def encrypt(string, bts=True):
    if not os.environ.get('chatreEncryptionKey'):
        print('You must create an encryption key')

    if type(string) == str:
        encoded = string.encode()
    else:
        encoded = string

    f = Fernet(encryption_key)
    
    if bts:
        return f.encrypt(encoded)

    else:
        return f.encrypt(encoded).decode()


def decrypt(string, bts=False):
    if not os.environ.get('chatreEncryptionKey'):
        print('You must create an encryption key')

    encryption_key = os.environ.get('chatreEncryptionKey').encode()
    if type(string) == str:
        encoded = string.encode()
    else:
        encoded = string
    f = Fernet(encryption_key)
    decrypted = f.decrypt(encoded)

    if bts:
        return decrypted

    else:
        return decrypted.decode()
    

def test():
    string = 'test'
    if len(sys.argv) > 1:
        string = sys.argv[1]
    
    print(string)

    encrypted = encrypt(string)

    print(encrypted)

    print(decrypt(encrypted))

if __name__ == "__main__":
    test()