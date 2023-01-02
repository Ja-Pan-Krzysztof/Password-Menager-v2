from getpass import getpass, getuser
from hashlib import sha512
import platform
import yaml

from settings import PLATFORM_FILE


class FirstRun:
    """Set the username and the password, which
    will be used to access the application and
    her saved passwords.
    """
    def __init__(self):
        self._username: str = getuser()
        self._password: str = ...

        with open(PLATFORM_FILE, 'w') as file:
            startup = {
                'system': {
                    'fulname': platform.platform(),
                    'os': platform.system(),
                    'machine': platform.machine(),
                    'release': platform.release(),
                },
                'python': {
                    'version': platform.python_version(),
                }
            }

            file.write(yaml.dump(startup))

    def set_pass(self) -> None:
        """User is entered a username (default system
        name) and a password that will be used to
        generate the hex. The bassword default is
        convert to him hex.

        :return: None
        """
        username = input(f'Enter a username (default-{self._username}) : ')
        self._username = username if username.strip(' ') != '' else getuser()

        self._password = sha512(getpass('Enter a password : ').encode()).hexdigest()

    @property
    def get_username(self):
        """Get setted a username."""
        return self._username

    @property
    def get_password(self):
        """Get setted a password as sha512"""
        return self._password
