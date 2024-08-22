from app.utils.responses import APIBaseException
from email_validator import validate_email as ve, EmailNotValidError


def validate_none(exception_cls: APIBaseException, **kwargs):
    """
    Checks is any of the fields given is none
    """
    for field in kwargs:
        try:
            assert kwargs.get(field)
        except AssertionError:
            return exception_cls(msg=f'{field} is required', code=400)
    
    return None

def validate_email(exception_cls: APIBaseException, email: str):
    """
    Checks if the given email address is valid
    """
    try:
        ve(email, check_deliverability=True)
    except EmailNotValidError:
        return exception_cls(msg=f'{email} is invalid', code=400)

    return None

