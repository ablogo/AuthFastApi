from datetime import datetime
from typing import Optional, Union
from src.services.otp_service import OTP
import time
from log2mongo import log2mongo

class TOTP(OTP):

    def __init__(self, secret: str, digest: str, time_step: int, return_digits: int, log: log2mongo) -> None:
        self.secret = secret
        self.digest = digest
        self.time_step = time_step
        self.return_digits = return_digits
        self.log = log
        super().__init__()

    async def at(self, for_time: Union[int, datetime], secret: Optional[str] = None, time_window: int = 0) -> str:
        otp = ""
        try:
            secret = self.secret if secret is None else secret
            if isinstance(for_time, int):
                for_time = self.to_unix_time(datetime.fromtimestamp(for_time))
            otp = self.generate_OPT(secret, self.to_unix_time(for_time), self.return_digits, self.digest)
        except Exception as e:
            self.log.logger.error(e)
        return otp
    
    async def now(self, secret: Optional[str] = None) -> str:
        return self.generate_OPT(self.secret if secret is None else secret, self.to_unix_time(datetime.now()), self.return_digits, self.digest)
    
    async def verify(self, otp_to_validate: str, secret: Optional[str] = None, for_time: Optional[datetime] = None, time_window: int = 0) -> bool:
        result = False
        try:
            secret = self.secret if secret is None else secret
            for_time = datetime.now() if for_time is None else for_time
            otp = await self.at(for_time, secret, time_window)
            if otp_to_validate == otp:
                result = True
        except Exception as e:
            self.log.logger.error(e)
        return result
    
    def to_unix_time(self, date) -> int:
        return int(time.mktime(date.utctimetuple()) / self.time_step)