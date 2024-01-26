from fastapi import HTTPException, status

class BaseException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


# Пользователи
class UserAlreadyExistsException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь уже существует'

class IncorrectEmailOrPasswordException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверный email или пароль'

class UserIsNotPresentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED



# JWT token
class TokenExpiredException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен истёк'

class TokenAbsentException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Токен отсутствует'

class IncorrectTokenException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверный формат токена'


# бронирование
class RoomCannotBeBooked(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Не осталось свободных номеров'