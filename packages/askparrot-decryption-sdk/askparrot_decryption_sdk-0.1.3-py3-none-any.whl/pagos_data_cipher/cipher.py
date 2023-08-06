from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import copy
import binascii
import datetime
from time import gmtime, strftime
from Crypto.Protocol.KDF import scrypt

class pagos_data_cipher:
    """
    Cipher to process specific data object with fileds:
    'cardType', 'cardCountry', 'brand', 'bank_name', 'product_code', 'clean_bank_name', 'creditOrDebit', 'cardCountry_alpha3'
    """
    BLOCK_SIZE = 16 # 128
    FIELDS_TO_CIPHER = ['cardType', 'cardCountry', 'brand', 'bank_name', 'product_code', 'clean_bank_name', 'creditOrDebit', 'cardCountry_alpha3']

    def __init__(self, key):
        self.key = key

    def generate_key(self, gen_key, salt):
        print(gen_key, salt)
        key = scrypt(gen_key.encode('utf-8'), salt.encode('utf-8'), 16, N=2**14, r=8, p=1) 
        return key

    """
    Object encryption (for test purposes only)
    """
    def encrypt_object(self, data):
        encrypted_data = copy.deepcopy(data)
        encrypted_at = strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
        key = self.generate_key(self.key, encrypted_at)
        cipher = AES.new(key, AES.MODE_ECB)

        for field_to_encrypt in self.FIELDS_TO_CIPHER:
            if (field_to_encrypt in encrypted_data):
                encrypted_field = cipher.encrypt(pad(encrypted_data[field_to_encrypt].encode('utf8'), self.BLOCK_SIZE))
                encrypted_data[field_to_encrypt] = binascii.hexlify(encrypted_field).decode()

        encrypted_data['encrypted_at'] = encrypted_at
        return encrypted_data

    """
    Object decryption decrypts following fields
    'cardType', 'cardCountry', 'brand', 'bank_name', 'product_code', 'clean_bank_name', 'creditOrDebit', 'cardCountry_alpha3'
    """
    def decrypt_object(self, data):

        decrypted_data = copy.deepcopy(data)
        encrypted_at = data['encrypted_at']
        key = self.generate_key(self.key, encrypted_at)
        cipher = AES.new(key, AES.MODE_ECB)

        for field_to_decrypt in self.FIELDS_TO_CIPHER:
            if (field_to_decrypt in decrypted_data):
                decrypted_field = unpad(cipher.decrypt(binascii.unhexlify(decrypted_data[field_to_decrypt])), self.BLOCK_SIZE)
                decrypted_data[field_to_decrypt] = decrypted_field.decode()

        return decrypted_data