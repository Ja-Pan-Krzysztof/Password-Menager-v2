from config import change_config, new_keys
from config.first_run import FirstRun
from settings import PLATFORM_FILE

from encryption.encryption import Encryption, Decryption

import os


if __name__ == '__main__':
    #e = Encryption()
    #e.add_pass_to_db('Mnichu', 'discord', '...')

    d = Decryption()
    print(d.decrypt_password('fsdfds'))

    # if not os.path.exists(PLATFORM_FILE):
    #     #a = change_config.ChangeConfig('passwoords_user.pass', 'secret-key.key', 'sdfsd.db')
    #     #a.change_parameters()
    #
    #     fr = FirstRun()
    #     fr.set_pass()
    #
    #     # If the application is launched for the first time,
    #     # models will be created.
    #     from database.models import build
    #     build()
    #
    #     keys = new_keys.NewKeys(fr.get_username, fr.get_password)
    #     keys.set_parameters()
    #
    # else:
    #     print('second run')
