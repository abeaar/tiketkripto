import os

import qrcode

def generate_ticket_qr(user_id, event_name, tickets_ordered, id_tiket):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"UserID:{user_id}|EventName:{event_name}|Tickets:{tickets_ordered}")
    qr.make(fit=True)

    qr_image = qr.make_image(fill='black', back_color='white')

    # Menyimpan gambar QR code dengan nama file id_tiket
    qr_code_folder = "qrcodes"
    if not os.path.exists(qr_code_folder):  # Pastikan folder ada
        os.makedirs(qr_code_folder)

    file_path = os.path.join(qr_code_folder, f"qrcode_{id_tiket}.png")
    qr_image.save(file_path)

    return file_path