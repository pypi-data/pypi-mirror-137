import hashlib
def hash_text(s:str):
    return hashlib.md5(s.encode()).hexdigest()