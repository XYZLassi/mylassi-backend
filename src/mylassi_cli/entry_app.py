import cmd2
from cmd2 import with_argparser


class EntryApp(cmd2.Cmd):
    parser_create_user = cmd2.Cmd2ArgumentParser()
    parser_create_user.add_argument('username', help='name for the new user')
    parser_create_user.add_argument('email', help='email from the new user')
    parser_create_user.add_argument('password', help='new password')
    parser_create_user.add_argument('-a', '--admin', action='store_true', default=False, help='is admin')

    @with_argparser(parser_create_user)
    def do_create_user(self, args):
        from mylassi_data.models import User
        from mylassi_data.db import session

        username = args.username
        email = args.email
        password = args.password

        new_admin = User()
        new_admin.username = username
        new_admin.email = email
        new_admin.is_admin = args.admin
        new_admin.set_password(password)

        session.add(new_admin)
        session.commit()
