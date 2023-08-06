import argparse
from argparse import ArgumentParser

from rich import print



def printerr(text: str):
    """Print error message and exit program"""
    print(text)
    exit()


def main():
    parser = ArgumentParser(description='Terminal operations for Mytwitch')

    commands = parser.add_subparsers(dest='command')
    auth_parser = commands.add_parser('auth', help='Authentication')


    # |-----------------
    # | AUTHENTICATION

    from . import client_id
    
    # Operations
    auth_action = auth_parser.add_mutually_exclusive_group(required=True)
    auth_action.add_argument('-N', dest='new', action='store_true', help='Create new token (requires -S)')
    auth_action.add_argument('-R', dest='revoke', action='store_true', help='Revoke token (requires -T)')

    # Value parameters
    auth_parser.add_argument(
        '-C',
        default=client_id,  # Mytwitch application client ID
        dest='client_id',
        help="Twitch application client ID"
    )
    auth_parser.add_argument('-T', dest='token')
    auth_parser.add_argument('-S', dest='scope', nargs='+')


    args = parser.parse_args()

    if args.command == 'auth':

        # Create new token
        if args.new:
            if not args.scope:
                printerr(
                    '[red]Scope is required.[/red] Specify with: [b]-S[/b]\n'
                    "\tEx. [b]-N -S 'chat:read' 'chat:edit'[/b]")

            from .auth import UserToken

            print(f'{UserToken(args.client_id, args.scope)!s}')


        # Revoke token
        if args.revoke:
            if not args.token:
                printerr(
                    '[red]Token is required.[/red] Specify with: [b]-T[/b]\n'
                    "\tEx. [b]-R -T 'abcdefghijklmnopqrstuvwxyz0123456789'[/b]")

            from .auth import UserToken
            
            user_token = UserToken(args.client_id, token=args.token, immed_auth=False)
            success = user_token.revoke()

            # Output the success in lowercase
            # for other terminal applications
            # to be able to use and easily understand
            print(str(success).lower())


if __name__ == '__main__':
    main()