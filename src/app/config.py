import tomllib
from dataclasses import dataclass

from app.constants import BASE_DIR


@dataclass
class BotConfig:
    token: str
    id_admin: int
    database: str


def load_config() -> BotConfig:
    with open(BASE_DIR / 'config.toml', 'rb') as file:
        data = tomllib.load(file)
        project_config = data['project']
    return BotConfig(
        token=project_config['token'],
        id_admin=project_config['id_admin'],
        database=project_config['database']
    )
