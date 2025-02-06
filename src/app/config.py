import os
from pathlib import Path
import tomllib
from dataclasses import dataclass


@dataclass
class BotConfig:
    token: str
    id_admin: int
    database: str
    base_dir: Path


def load_config() -> BotConfig:
    with open(os.getenv('BASE_CONFIG'), 'rb') as file:
        data = tomllib.load(file)
        project_config = data['project']
    return BotConfig(
        token=project_config['token'],
        id_admin=project_config['id_admin'],
        database=project_config['database'],
        base_dir=Path(project_config['base_dir'])
    )
