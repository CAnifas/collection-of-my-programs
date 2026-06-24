import os
import json
import struct
import lzma
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def test():
    print("=== ЗАПУСК ТЕСТА ЯДРА TERNOS ===")
    
    password = "super_secure_password_123"
    
    # Create mock files
    files = [
        {"name": "test1.txt", "content": b"Hello world! This is a test file for Ternos archiver."},
        {"name": "test2.txt", "content": b"LZMA compression is extreme. " * 100}
    ]
    
    # 1. Pack
    metadata = {
        "version": "1.0",
        "files": [{"path": f["name"], "size": len(f["content"])} for f in files]
    }
    meta_bytes = json.dumps(metadata, ensure_ascii=False).encode('utf-8')
    header = struct.pack(">I", len(meta_bytes))
    payload = header + meta_bytes + b"".join([f["content"] for f in files])
    
    print(f"Оригинальный размер payload: {len(payload)} байт")
    
    # 2. Compress
    compressed = lzma.compress(payload, preset=9)
    print(f"Сжатый (LZMA) размер payload: {len(compressed)} байт (Сжатие: {len(compressed)/len(payload)*100:.1f}%)")
    
    # 3. Encrypt
    salt = os.urandom(16)
    iv = os.urandom(12)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 600000, 32)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, compressed, None)
    
    magic = b"TERNOS\x00"
    archive_bytes = magic + salt + iv + ciphertext
    print(f"Итоговый размер зашифрованного архива: {len(archive_bytes)} байт")
    
    # Verification 1: Tamper proofing (anti-tamper)
    print("Проверка целостности (попытка взлома)...")
    # Let's modify 1 byte of the ciphertext
    tampered_bytes = bytearray(archive_bytes)
    tampered_bytes[-1] ^= 0x01 # Flip the last bit
    
    # Try to decrypt tampered bytes
    try:
        t_magic = tampered_bytes[:7]
        t_salt = tampered_bytes[7:23]
        t_iv = tampered_bytes[23:35]
        t_ciphertext = tampered_bytes[35:]
        
        t_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), t_salt, 600000, 32)
        t_aesgcm = AESGCM(t_key)
        t_aesgcm.decrypt(t_iv, t_ciphertext, None)
        print("ОШИБКА: Измененный архив успешно расшифровался! Защита сломана.")
        exit(1)
    except Exception as e:
        print(f"УСПЕХ: Изменение архива обнаружено. Дешифрация отклонена. Ошибка: {type(e).__name__}")
        
    # Verification 2: Incorrect password
    print("Проверка защиты от неверного пароля...")
    try:
        t_key = hashlib.pbkdf2_hmac('sha256', "wrong_password".encode('utf-8'), salt, 600000, 32)
        t_aesgcm = AESGCM(t_key)
        t_aesgcm.decrypt(iv, ciphertext, None)
        print("ОШИБКА: Неверный пароль был принят! Защита сломана.")
        exit(1)
    except Exception as e:
        print(f"УСПЕХ: Неверный пароль отклонен. Ошибка: {type(e).__name__}")

    # Verification 3: Correct decryption & decompression
    print("Проверка штатной распаковки...")
    r_magic = archive_bytes[:7]
    r_salt = archive_bytes[7:23]
    r_iv = archive_bytes[23:35]
    r_ciphertext = archive_bytes[35:]
    
    r_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), r_salt, 600000, 32)
    r_aesgcm = AESGCM(r_key)
    r_decrypted = r_aesgcm.decrypt(r_iv, r_ciphertext, None)
    r_uncompressed = lzma.decompress(r_decrypted)
    
    # Extract
    r_meta_len = struct.unpack(">I", r_uncompressed[:4])[0]
    r_meta_bytes = r_uncompressed[4:4+r_meta_len]
    r_meta = json.loads(r_meta_bytes.decode('utf-8'))
    
    r_offset = 4 + r_meta_len
    print("Извлеченные файлы:")
    for f_info in r_meta["files"]:
        f_data = r_uncompressed[r_offset:r_offset+f_info["size"]]
        r_offset += f_info["size"]
        print(f" - {f_info['path']}: {len(f_data)} байт")
        # Match content
        orig = next(x for x in files if x["name"] == f_info["path"])
        if orig["content"] != f_data:
            print(f"ОШИБКА: Содержимое файла {f_info['path']} повреждено!")
            exit(1)
            
    print("УСПЕХ: Все тесты пройдены! Алгоритм шифрования, сжатия и проверки целостности Ternos работает безупречно.")

if __name__ == "__main__":
    test()
