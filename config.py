import click

from pathlib import Path
from base64 import encodebytes, decodebytes

import database


def read_secret():
    config_path = Path.joinpath(Path.home(), ".passm")
    if not config_path.exists():
        show_setup_msg()

    config_file = Path.joinpath(config_path, "secret")
    if not config_file.is_file():
        show_setup_msg()

    secret = config_file.read_bytes()
    return decodebytes(secret).decode(encoding="utf-8")


def show_setup_msg():
    click.echo("First run Command \"passm setup\" to complete the setup")


def create_setup(secret):
    config_path = Path.joinpath(Path.home(), ".passm")
    if not config_path.exists():
        config_path.mkdir()

    config_file = Path.joinpath(config_path, "secret")
    if not config_file.is_file():
        config_file.touch()
    data = encodebytes(bytes(secret, encoding='utf8'))
    config_file.write_bytes(data)

    db_file = Path.joinpath(config_path, "database.db")
    if not db_file.is_file():
        db_file.touch()

    database.Repository().setup()


def get_db_path():
    return Path.joinpath(Path.home(), ".passm", "database.db")