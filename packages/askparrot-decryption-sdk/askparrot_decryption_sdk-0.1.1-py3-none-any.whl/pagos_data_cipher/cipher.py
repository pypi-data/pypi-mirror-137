from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import copy
import binascii

class pagos_data_cipher:
    """
    Cipher to process specific data object with fileds:
    'cardType', 'cardCountry', 'brand', 'bank_name', 'product_code', 'clean_bank_name'
    """
    BLOCK_SIZE = 16 # 128
    FIELDS_TO_CIPHER = ['cardType', 'cardCountry', 'brand', 'bank_name', 'product_code', 'clean_bank_name']

    def __init__(self, key):
        self.key = key
        self.cipher = AES.new(self.key.encode('utf8'), AES.MODE_ECB)

    """
    Object encryption (for test purposes only)
    """
    def encrypt_object(self, data):
        encrypted_data = copy.deepcopy(data)
        for field_to_encrypt in self.FIELDS_TO_CIPHER:
            if (field_to_encrypt in encrypted_data):
                encrypted_field = self.cipher.encrypt(pad(encrypted_data[field_to_encrypt].encode('utf8'), self.BLOCK_SIZE))
                encrypted_data[field_to_encrypt] = binascii.hexlify(encrypted_field).decode()

        return encrypted_data

    """
    Object decryption decrypts following fields
    'cardType', 'cardCountry', 'brand', 'bank_name', 'product_code', 'clean_bank_name'
    """
    def decrypt_object(self, data):
        decrypted_data = copy.deepcopy(data)
        for field_to_decrypt in self.FIELDS_TO_CIPHER:
            if (field_to_decrypt in decrypted_data):
                decrypted_field = unpad(self.cipher.decrypt(binascii.unhexlify(decrypted_data[field_to_decrypt])), self.BLOCK_SIZE)
                decrypted_data[field_to_decrypt] = decrypted_field.decode()

        return decrypted_data