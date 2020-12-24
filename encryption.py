from cryptography.fernet import Fernet
import os, sys

encryption_key = os.environ.get('chatreEncryptionKey').encode()

def encrypt(string, bts=True):
    if not encryption_key:
        print('setting encryption key...')
        os.environ["chatreEncryptionKey"] = Fernet.generate_key().decode()

    try:
        if type(string) == type('a'):
            encoded = string.encode()
        else:
            encoded = string

        f = Fernet(encryption_key)
        
        if bts:
            return f.encrypt(encoded)

        else:
            return f.encrypt(encoded).decode()

    except:
        print(sys.exc_info()[0])


def decrypt(string, bts=True):
    try:
        if type(string) == type('a'):
            encoded = string.encode()
        else:
            encoded = string
        f = Fernet(encryption_key)
        decrypted = f.decrypt(encoded)

        if bts:
            return decrypted

        else:
            return decrypted.decode()
    
    except:
        print(sys.exc_info()[0])

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