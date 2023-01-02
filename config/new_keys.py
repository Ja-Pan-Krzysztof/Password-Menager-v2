from uuid import UUID, uuid4, uuid5
from time import sleep
from random import random
from math import sqrt
from base64 import b64encode

import os
import yaml

from settings import BASE_DIR

from typing import TypeVar, Generic

T = TypeVar('T')


class NewKeys(Generic[T]):
    """Generate and set a hex on first run app"""

    def __init__(self, name: T=..., password: T=...):
        """From the name and the password, will be generated
        64 bits hex.

        :param name: Username that will be use only to generate hex (default: computer name)
        :param password: Password that will be used to generate hex and logging to application
        """

        self.name: T = name
        self.password: T = password

        self._hex_name: T = ...
        self._hex_pass: T = ...
        self._base64: T = ...
        self._uuid4: T = ...

    @staticmethod
    def _read_config() -> dict:
        """Return user config if exist else return default config.

        :return: config (dict)
        """
        if os.path.exists(f'{BASE_DIR}/config/config-user.yaml'):
            with open(f'{BASE_DIR}/config/config-user.yaml', 'r') as file:
                return yaml.safe_load(file)

        else:
            path = f'{BASE_DIR}/config/config.yaml'

            try:
                with open(path, 'r') as file:
                    return yaml.safe_load(file)

            except (FileNotFoundError, FileExistsError):
                raise f'File `{path}` do not exist'

    def set_parameters(self) -> None:
        """Generate 64 bits hex form the self.name and the self.password.
        Save the hex and base 64 to file or/and db.

        :return: None
        """
        self._uuid4 = uuid4().hex
        self._hex_name = uuid5(UUID(self._uuid4), self.name).hex
        sleep(sqrt(random() + random() * random()))
        self._hex_pass = uuid5(UUID(self._uuid4), self.password).hex

        self._base64 = f'{b64encode(bytes.fromhex(self._hex_name + self._hex_pass)).decode()}'

        config = self._read_config()

        file_key = config.get('storage').get('file').get('key')
        db_key = config.get('storage').get('db').get('name')

        if file_key is not None:
            self._write_key_to_file(file_key)

        if db_key is not None:
            self._write_key_to_database()

    def _write_key_to_file(self, name: str) -> None:
        """Here, the hex and the base64 are saved to file.

        :param name: filename where the hex and the base64 are to
        be saved

        :return: None
        """
        with open(f'{BASE_DIR}/{name}', 'w') as file:
            file.write(f'key_hex:{self._hex_name}{self._hex_pass}')
            file.write(f'\nkey_base64:{self._base64}')
            file.write(f'\nuuid4:{self._uuid4}')

    def _write_key_to_database(self) -> None:
        """Here, the hex and the base64 are saved to database
        by new session.

        :return: None
        """
        from sqlalchemy.orm.session import sessionmaker
        from database.connection import Connection
        from database.models import Owner

        conn = Connection()
        engine = conn.conn()

        Session = sessionmaker(bind=engine)
        session = Session()

        owner = Owner(
            username=self.name,
            password=self.password,
            key_base64=self._base64,
            key_hex=f'{self._hex_name}{self._hex_pass}',
            uuid4=self._uuid4,
        )

        try:
            session.add(owner)
            session.commit()
            session.close()

        # Was commited to empty database. No such table `owner`.
        except Exception as error:
            raise error

        finally:
            session.close()

    @property
    def _get_hex(self) -> T:
        """Get hex from setted parameters.

        :return: hex string
        """
        return f'{self._hex_name}{self._hex_pass}'

    @property
    def _get_b64(self) -> T:
        """Get base64 from setted parameters.

        :return: base64 string
        """
        return self._base64
