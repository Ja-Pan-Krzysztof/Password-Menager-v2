import os.path

import yaml
from typing import Generic, TypeVar, Union

from settings import CONFIG_DIR


T = TypeVar('T')

# with open(f'{BASE_DIR}/config/config.yaml', 'r') as f:
#     a = yaml.safe_load(f)
#     print(a)
#     print(type(a))


class ChangeConfig(Generic[T]):
    """Set file and db name where passwords and key will be storaged."""
    def __init__(self, pass_file: T, key_file: T, db_name: T):
        """Set the name of files, if the file is name
        None.lower(), This file wont be created.

        The file extentions can be skipped. Default will be added
        extention `.key` for the key-file and `.pass` for the
        password-file. For db-name it will be extention `.db`

        :param pass_file: How the file is name, where the passwords will be storaged
        :param key_file: How the file is name, where the key will be storaged
        :param db_name: How the file is name, where the passwords will be storaged
        """

        self.pass_file = self._parse_arg(pass_file, '.txt')
        self.key_file = self._parse_arg(key_file, '.key')
        self.db_name = self._parse_arg(db_name, '.db')

    @staticmethod
    def _parse_arg(file: str, extension: str) -> Union[str, None]:
        """Check if that file has a good extension. When
        extension is invalid, it will be setted with
        default extension. If file name is `None`, will be
        returned None.

        :param file: filename that is to be checked
        :param extension: name of extentsion, that
        will be setted, when filename has an invalid
        extentsion
        :return: Valid filename with extension (str) or None
        """
        file_name, file_extension = os.path.splitext(file)

        if file_name.lower() == 'none':
            return None

        if file_extension in ['', '.']:
            file_extension = extension

        return f'{file_name}{file_extension}'

    @staticmethod
    def _open_config() -> dict:
        """Open config file and convert to dict type.

        :return: dict of config
        """
        with open(f'{CONFIG_DIR}/config.yaml', 'r') as file:
            return yaml.unsafe_load(file)

    def change_parameters(self) -> None:
        """Change values in confing from entered to init
        and write these to `yaml` file. Creating database."""
        config_file = self._open_config()

        if self.key_file is not None:
            config_file.get('storage').get('file')['key'] = self.key_file

        else:
            del config_file.get('storage').get('file')['key']

        if self.db_name is not None:
            config_file.get('storage').get('db')['name'] = self.db_name

        else:
            del config_file.get('storage').get('db')['name']

        if self.pass_file is not None:
            config_file.get('storage').get('file')['passwords'] = self.pass_file

        else:
            del config_file.get('storage').get('file')['passwords']

        with open(f'{CONFIG_DIR}/config-user.yaml', 'w') as file:
            file.write(yaml.dump(config_file))
