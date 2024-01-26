import hashlib
class Hash():
    def hash_password(password) -> str:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    def verify_password(entered_password,stored_hashed_password):
        entered_password_hash = hashlib.sha256(entered_password.encode()).hexdigest()
        return entered_password_hash == stored_hashed_password