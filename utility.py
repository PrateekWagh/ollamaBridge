from pwdlib import PasswordHash
password_hash = PasswordHash.recommended()
def passwordToHash(password):
    return password_hash.hash(password=password)

def verify_password(curr_password, hashed_password):
    return password_hash.verify(curr_password, hashed_password)