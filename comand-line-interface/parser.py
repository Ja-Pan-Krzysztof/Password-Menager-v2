from argparse import ArgumentParser


class Parser:
    PARSER = ArgumentParser('top', description='Storage your password in save place.')
    SUBPARSER = PARSER.add_subparsers(dest='command')

    def __init__(self):

        # Categories of options
        self.config = self.SUBPARSER.add_parser('config')
        self.npassword = self.SUBPARSER.add_parser('npassword')
        self.gpassword = self.SUBPARSER.add_parser('gpassword')
        self.init = self.SUBPARSER.add_parser('init')
        self.factory_settings = self.SUBPARSER.add_parser('factory_settings')

        # Config options
        self.config.add_argument('-p', '--password_file', type=str, required=True,
                            help='filename where will be stored passwords', dest='<password-filename>')
        self.config.add_argument('-k', '--key_file', type=str, required=True, help='filename where will be stored the key',
                            dest='<key-filename>')
        self.config.add_argument('-d', '--db_name', type=str, required=True,
                            help='database name where will be stored passwords and key', dest='<db name>')

        # Gpassword options
        self.gpassword.add_argument('-l', '--login', type=str, required=True,
                                    help='Login to the site.', dest='<login>')
        self.gpassword.add_argument('-s', '--site', type=str, required=True,
                                    help='Site.', dest='<site>')
        self.gpassword.add_argument('-p', '--password', type=str, required=True,
                                    help='Password to the site.', dest='<password>')


        self.args = self.PARSER.parse_args()


        print('###', self.args)


args = Parser()


if args.args.command == 'config':
    print('work 1')

elif args.args.command == 'npassword':
    print('work 2')

elif args.args.command == 'gpassword':
    print('work 3')

elif args.args.command == 'init':
    print('work 4')





