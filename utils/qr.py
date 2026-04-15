import qrcode
import os

def generate_qr(session_id, base_url):
    url = f"{base_url}mark?session_id={session_id}"

    img = qrcode.make(url)

    folder = "static/qr_codes"
    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/{session_id}.png"
    img.save(path)

    return path
