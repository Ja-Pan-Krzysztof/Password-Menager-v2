from sqlalchemy import create_engine

import yaml
import os

from settings import BASE_DIR, CONFIG_DIR


class Connection:
    """Get name of database from yaml file
    and create handler for database."""
    def __init__(self, echo: bool=False):
        self.echo = echo

    @staticmethod
    def _get_db_name() -> str:
        """Check if config file form user exist then get
        database name. When config file form user
        does not exist, will be used default config file.

        :return: name of database (str)
        """
        db_name = ...

        try:
            if os.path.exists(f'{CONFIG_DIR}/config-user.yaml'):
                with open(f'{CONFIG_DIR}/config-user.yaml') as file:
                    dictionary: dict = yaml.safe_load(file)

            else:
                with open(f'{CONFIG_DIR}/config.yaml') as file:
                    dictionary: dict = yaml.safe_load(file)

            db_name = dictionary.get('storage').get('db').get('name')

        except (FileNotFoundError, FileNotFoundError):
            raise f'Cannot open default config.yaml'

        finally:
            return db_name

    def conn(self):
        """Create handler for database engine and return it."""
        return create_engine(f'sqlite:////{BASE_DIR}/{self._get_db_name()}', echo=self.echo)
