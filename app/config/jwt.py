from datetime import datetime, timedelta

from jose import jwt

from app.config.consts import JWT_ALGORITHM, JWT_SECRET_KEY

ACCESS_TOKEN_EXPIRE_MINUTES = 43200
REFRESH_TOKEN_EXPIRE_MINUTES = 172800


def create_access_token(user_id: int):
    access_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_to_encode = {
        'user_id': user_id,
        'exp': access_token_expires
    }

    return jwt.encode(access_token_to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM), access_token_expires


def create_refresh_token(user_id: int):
    refresh_token_expires = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token_to_encode = {
        'user_id': user_id,
        'exp': refresh_token_expires
    }

    return jwt.encode(refresh_token_to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM), refresh_token_expires


def create_jwt(user_id: int):
    access_token, access_exp = create_access_token(user_id)
    refresh_token, refresh_exp = create_refresh_token(user_id)

    return {
        "access_token": access_token,
        "access_exp": access_exp,
        "refresh_token": refresh_token,
        "refresh_exp": refresh_exp
    }


def add_jwt(response, access_token: str, refresh_token: str):
    response.set_cookie(key='access_token', value=access_token)
    response.set_cookie(key='refresh_token', value=refresh_token)

    return response


def delete_jwt(response):
    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')

    return response
