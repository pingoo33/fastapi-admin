from enum import Enum


class ErrorCode(Enum):
    INVALID_FORMAT_REQUEST = 40000

    INVALID_TOKEN = 40100
    NOT_FOUND_TOKEN = 40101
    INVALID_PASSWORD = 40102

    USER_NOT_FOUND = 40400


class BaseRuntimeException(Exception):
    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message


class BadRequestException(BaseRuntimeException):
    def __init__(self, code: ErrorCode, message: str):
        super().__init__(code, message)


class UnauthorizedException(BaseRuntimeException):
    def __init__(self, code: ErrorCode, message: str):
        super().__init__(code, message)


class NotFoundException(BaseRuntimeException):
    def __init__(self, code: ErrorCode, message: str):
        super().__init__(code, message)
