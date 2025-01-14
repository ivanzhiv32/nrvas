from pathlib import Path


class StartCommand:
    def __init__(self, path: Path, id_admin: int) -> None:
        self._path = path
        self._id_admin = id_admin

    @property
    def id_admin(self) -> int:
        return self._id_admin

    @property
    def file(self) -> Path:
        return self._path / 'stickers/hello.webp'

    def get_text(self, text: str) -> str:
        return (f'Здравствуйте, {text}\n'
                'Я - SciComBot, и я провожу отбор кандидатов в научную роту.\n'
                'Выберете интересующий Вас раздел 👇')
