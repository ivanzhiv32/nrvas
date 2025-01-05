import os
from pathlib import Path
from dataclasses import dataclass



@dataclass
class BotSecret:
    token: str
    id_admin: int


def load_bot_secret() -> BotSecret:
    return BotSecret(
        token=os.getenv('TOKEN'),
        id_admin=int(os.getenv('ID_ADMIN')),
    )
