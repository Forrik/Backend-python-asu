from typing import Any, Optional
from django.core.exceptions import ValidationError

class BussinesLogicException(ValidationError):
    message = "Внутренняя ошибка сервиса. Обратитесь к админстратору систему"
    details = ""
    def __init__(self, code: Optional[str] = None, params: Any = None, details: str="") -> None:
        super().__init__(self.message, code, params)
        self.details = details