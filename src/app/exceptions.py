class ScoreException(BaseException):
    def __str__(self) -> str:
        return 'Невалидный средний балл'
