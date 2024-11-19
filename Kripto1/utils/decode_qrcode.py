from pyzbar.pyzbar import decode
from PIL import Image

def decode_qr_code(qr_image_path):
    # Membaca gambar QR Code
    image = Image.open(qr_image_path)
    # Menggunakan pyzbar untuk mendekode QR Code
    decoded_objects = decode(image)

    # Jika QR Code ditemukan, return data yang terdekripsi
    if decoded_objects:
        return decoded_objects[0].data.decode('utf-8')
    else:
        return None
