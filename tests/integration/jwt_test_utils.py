from datetime import datetime, timedelta

from jose import jwt


def generate_test_jwt(secret="SECRET", user_id="test-user", expires_delta=3600):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=expires_delta),
    }
    return jwt.encode(payload, secret, algorithm="HS256")
