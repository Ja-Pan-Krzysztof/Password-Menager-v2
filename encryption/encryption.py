from getpass import getpass
from hashlib import sha512
from cryptography.fernet import Fernet
from typing import Generic, TypeVar, Union

from sqlalchemy.orm.session import sessionmaker
from database.connection import Connection
from database.models import Owner, Passwords

from uuid import UUID, uuid5


T = TypeVar('T')


class Encryption(Generic[T]):
    """Encrypt the password for the site."""

    # Connect to database
    CONN = Connection()
    ENGINE = CONN.conn()

    def __init__(self):
        """Build session for DB."""

        self._Session = sessionmaker(bind=self.ENGINE)
        self._session = self._Session()

    def _get_key(self) -> str:
        """Get the base64 key from database.

        :return: base64 key (str)
        """
        key = self._session.query(Owner).get(1).key_base64  # get the key that is to be encrypted passwords

        self._session.close()

        return key

    def add_pass_to_db(self, _login: T, _site: T, _password: T) -> None:
        """Add new record to database (login, site, password).

        :param _login: the login for this site
        :param _site: site
        :param _password: the password for this site
        :return: None
        """
        fernet = Fernet(self._get_key())

        password = Passwords(
            login=_login,
            site=_site,
            password=fernet.encrypt(_password.encode())
        )

        self._session.add(password)
        self._session.commit()

        self._session.close()


class Decryption(Generic[T]):
    """Decrypt any password for the site."""

    # Connect to database
    CONN = Connection()
    ENGINE = CONN.conn()

    def __init__(self):
        """Create session for database."""

        self._Session = sessionmaker(bind=self.ENGINE)
        self._session = self._Session()

    def decrypt_password(self, _site: T) -> Union[int, list]:
        """Using the login and entered password, create a key. If this key
        and key in database are same, return password list for the site.

        :param _site: to which site are to be returned passwords
        :return: list of passwords
        """
        query = self._session.query(Owner).get(1)  # get all information about owner

        username = query.username
        password1 = query.password

        password2 = sha512(getpass('Enter a main password : ').encode()).hexdigest()
        key = f'{uuid5(UUID(query.uuid4), username).hex}{uuid5(UUID(query.uuid4), password2).hex}'  # make key with the username and the password

        if not key == query.key_hex:
            return 0

        if not password2 == password1:
            return 0

        site = self._session.query(Passwords).filter_by(site=_site)
        passwords = []

        for s in site:
            fernet = Fernet(query.key_base64)

            password = fernet.decrypt(s.password).decode()
            passwords.append((f'{s.login}', f'{s.login}', f'{password}'))

        return passwords
