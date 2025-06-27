from datetime import datetime, timedelta, timezone

from jose import jwt


def generate_test_jwt(secret="SECRET", user_id="test-user", expires_delta=3600):
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_delta),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


print(generate_test_jwt())
