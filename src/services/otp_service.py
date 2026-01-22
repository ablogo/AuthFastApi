import hmac, struct, base64


class OTP():
    def __init__(self) -> None:
        pass

    def get_hmac_sha(self, secret: bytes, moving_factor: bytes, digest: str):
        return hmac.new(secret, moving_factor, digest)

    def to_bytes(self, value: str, is_value_ascii: bool = False, is_value_hex: bool = False):
        if is_value_ascii:
            return value.encode('ascii')
        elif is_value_hex:
            return bytes(bytearray.fromhex(value))
        else:
            return base64.b32decode(value, casefold=True)
    
    def generate_OPT(self, secret: str, moving_factor: int, return_digits: int, digest: str, is_secret_ascii: bool = False, is_secret_hex: bool = False):
        otp_code = ""
        try:
            msg = struct.pack('>Q', moving_factor)
            key = self.to_bytes(secret, is_secret_ascii, is_secret_hex)
            hasher = self.get_hmac_sha(key, msg, digest)
            #hasher_hex = hasher.hexdigest()
            #hmac_hash = bytes.fromhex(hasher_hex)
            hmac_hash = bytearray(hasher.digest())
            offset = hmac_hash[-1] & 0xF
            bin_code = (
                (hmac_hash[offset] & 0x7F) << 24 |
                (hmac_hash[offset + 1] & 0xFF) << 16 |
                (hmac_hash[offset + 2] & 0xFF) << 8 |
                (hmac_hash[offset + 3] & 0xFF)
            )
            otp_code = str(bin_code)[-return_digits :]

            while (otp_code.__len__() < return_digits):
                otp_code = "0" + otp_code

        except Exception as e:
            raise e
        return otp_code