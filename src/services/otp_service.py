import hmac, struct


class OTP():
    DIGITS_POWER = [1,10,100,1000,10000,100000,1000000,10000000,100000000]

    def __init__(self) -> None:
        pass

    def get_hmac_sha(self, secret: bytes, moving_factor: bytes, digest: str):
        return hmac.new(secret, moving_factor, digest)

    def to_bytes(self, value: str):
        bytes_object = value.encode('ascii')
        hex_string = bytes_object.hex()
        return bytes(bytearray.fromhex(hex_string))
    
    def generate_OPT(self, secret: str, moving_factor: int, return_digits: int, digest: str):
        otp_code = ""
        try:
            msg = struct.pack('>Q', moving_factor)
            k = self.to_bytes(secret)
            hasher = self.get_hmac_sha(k, msg, digest)
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
            otp_code = str(bin_code % self.DIGITS_POWER[return_digits])

            while (otp_code.__len__() < return_digits):
                otp_code = "0" + otp_code

        except Exception as e:
            raise e
        return otp_code