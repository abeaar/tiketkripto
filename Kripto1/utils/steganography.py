from PIL import Image

def encode_image(image_path, data, encoded_image_path):
    # Membuka gambar dan memastikan dalam mode RGB
    img = Image.open(image_path)
    img = img.convert('RGB')  # Konversi gambar ke mode RGB
    
    # Mengubah data menjadi bytes
    byte_data = data.encode('utf-8') if isinstance(data, str) else data
    
    # Mengakses pixel dari gambar
    pixels = img.load()
    
    # Menyimpan data yang ingin disembunyikan dalam gambar
    data_index = 0
    data_len = len(byte_data)
    
    # Menyembunyikan data dalam pixel gambar
    for y in range(img.height):
        for x in range(img.width):
            # Mengambil pixel (r, g, b)
            r, g, b = pixels[x, y]
            
            if data_index < data_len:
                # Menyembunyikan bit pertama dari byte dalam bit paling rendah warna merah
                r = (r & 0xFE) | (byte_data[data_index] >> 7)
                data_index += 1

            if data_index < data_len:
                # Menyembunyikan bit kedua dalam bit paling rendah warna hijau
                g = (g & 0xFE) | ((byte_data[data_index] >> 6) & 1)
                data_index += 1

            if data_index < data_len:
                # Menyembunyikan bit ketiga dalam bit paling rendah warna biru
                b = (b & 0xFE) | ((byte_data[data_index] >> 5) & 1)
                data_index += 1

            # Menyimpan kembali pixel yang sudah dimodifikasi
            pixels[x, y] = (r, g, b)

            # Jika semua data sudah disembunyikan, keluar dari loop
            if data_index >= data_len:
                break

    # Menyimpan gambar yang sudah dienkode
    img.save(encoded_image_path)
    print(f"QR Code encoded with data and saved to {encoded_image_path}")

def decode_image(image_path):
    # Fungsi untuk mendekripsi data yang disembunyikan dalam gambar
    img = Image.open(image_path)
    
    # Proses decoding steganografi yang sesuai
    pixels = img.load()

    # Menyimpan data yang didekode
    decoded_data = bytearray()
    byte = 0
    bit_count = 0

    for y in range(img.height):
        for x in range(img.width):
            # Mengambil pixel (r, g, b)
            r, g, b = pixels[x, y]
            
            # Mengambil bit dari setiap kanal warna
            byte |= ((r & 1) << 7 - bit_count)  # Menyembunyikan bit dari merah
            bit_count += 1

            if bit_count == 8:
                decoded_data.append(byte)
                byte = 0
                bit_count = 0
                if len(decoded_data) >= img.width * img.height:
                    break

            byte |= ((g & 1) << 7 - bit_count)  # Menyembunyikan bit dari hijau
            bit_count += 1

            if bit_count == 8:
                decoded_data.append(byte)
                byte = 0
                bit_count = 0
                if len(decoded_data) >= img.width * img.height:
                    break

            byte |= ((b & 1) << 7 - bit_count)  # Menyembunyikan bit dari biru
            bit_count += 1

            if bit_count == 8:
                decoded_data.append(byte)
                byte = 0
                bit_count = 0
                if len(decoded_data) >= img.width * img.height:
                    break

    # Mengonversi byte data kembali ke string
    return decoded_data.decode('utf-8', errors='ignore')  # Mengabaikan error jika ada byte yang rusak

