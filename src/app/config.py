import os
from pathlib import Path
from dataclasses import dataclass



@dataclass
class BotConfig:
    token: str
    id_admin: int


def load_bot_secret() -> BotConfig:
    return BotConfig(
        token=os.getenv('TOKEN'),
        id_admin=int(os.getenv('ID_ADMIN')),
    )
