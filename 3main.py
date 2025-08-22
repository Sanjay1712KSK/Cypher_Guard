from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import StreamingResponse
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import os, io

app = FastAPI()

# 🔑 make a secret key from password
def make_key(password: str, salt: bytes):
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
    return kdf.derive(password.encode())

# 🔒 encrypt file
def encrypt_file(data: bytes, password: str):
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = make_key(password, salt)
    ct = AESGCM(key).encrypt(nonce, data, None)
    return b"ENC" + salt + nonce + ct  # save format: header+salt+nonce+ciphertext

# 🔓 decrypt file
def decrypt_file(data: bytes, password: str):
    if not data.startswith(b"ENC"):
        raise ValueError("Not an encrypted file")
    salt, nonce, ct = data[3:19], data[19:31], data[31:]
    key = make_key(password, salt)
    return AESGCM(key).decrypt(nonce, ct, None)

# 📤 endpoint: encrypt
@app.post("/encrypt")
async def encrypt(file: UploadFile, password: str = Form(...)):
    data = await file.read()
    enc = encrypt_file(data, password)
    return StreamingResponse(io.BytesIO(enc),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={file.filename}.enc"})

# 📥 endpoint: decrypt (✅ updated)
@app.post("/decrypt")
async def decrypt(file: UploadFile, password: str = Form(...)):
    data = await file.read()
    dec = decrypt_file(data, password)
    # Remove .enc if it exists
    original_name = file.filename
    if original_name.endswith(".enc"):
        original_name = original_name[:-4]
    else:
        original_name = f"decrypted_{file.filename}"
    return StreamingResponse(io.BytesIO(dec),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={original_name}"})

