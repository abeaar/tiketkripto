from utils.steganography import decode_image

def decode_steg_image(image_path):
    # Fungsi untuk mendekripsi data yang disembunyikan di dalam gambar
    decoded_data = decode_image(image_path)
    return decoded_data
