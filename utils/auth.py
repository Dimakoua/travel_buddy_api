import jwt
from datetime import datetime, timedelta
from config import settings

class Token:
    @staticmethod
    def generate_and_sign(user_id: str) -> str:
        expire = datetime.utcnow() + timedelta(days=1)
        payload = {"user_id": user_id, "exp": expire}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def verify_token(token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
