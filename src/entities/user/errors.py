from fastapi import HTTPException, status


class UserRegisteredBeforeError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="User registered before!")


class PasswordNotMatchError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Wrong password!")


class UserDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST,
                         detail="User does not exist!")
