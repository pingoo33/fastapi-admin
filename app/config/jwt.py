from datetime import datetime, timedelta

from fastapi import status, HTTPException, Request, Cookie
from jose import jwt

from app.config.consts import JWT_ALGORITHM, JWT_SECRET_KEY

ACCESS_TOKEN_EXPIRE_MINUTES = 43200
REFRESH_TOKEN_EXPIRE_MINUTES = 172800


class AuthenticationSubject:
    def __init__(self, subject_id, access_token, access_expire, refresh_token, refresh_expire):
        self.subject_id = subject_id
        self.access_token = access_token
        self.access_expire = access_expire
        self.refresh_token = refresh_token
        self.refresh_expire = refresh_expire


def get_subject(access_token: str, refresh_token: str):
    try:
        payload_access = jwt.decode(access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        try:
            payload_refresh = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='다시 로그인 해주세요.')
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='다시 로그인 해주세요.')
        return AuthenticationSubject(payload_access['user_id'],
                                     "", payload_access['exp'],
                                     "", payload_refresh['exp'])
    except jwt.ExpiredSignatureError:
        try:
            payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            access_token, access_expire = create_access_token(payload['user_id'])
            refresh_token, refresh_expire = create_refresh_token(payload['user_id'])
            return AuthenticationSubject(payload['user_id'], access_token, access_expire, refresh_token, refresh_expire)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='다시 로그인 해주세요.')
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='다시 로그인 해주세요.')
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='다시 로그인 해주세요.')


def create_access_token(user_id: str):
    access_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_to_encode = {
        'user_id': user_id,
        'exp': access_token_expires
    }

    return jwt.encode(access_token_to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM), access_token_expires


def create_refresh_token(user_id: str):
    refresh_token_expires = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token_to_encode = {
        'user_id': user_id,
        'exp': refresh_token_expires
    }

    return jwt.encode(refresh_token_to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM), refresh_token_expires


def create_jwt(user_id: str):
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


class AdminJWTProvider:
    async def __call__(self,
                       request: Request,
                       access_token: str = Cookie(None),
                       refresh_token: str = Cookie(None)):
        return get_subject(access_token, refresh_token)
