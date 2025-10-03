"""
Run discotify command line
You can add/remove user/webhook aliases
You can send messages to discord directly from the shell
"""

import sys
import argparse

from .discotify import Discotify

def main():
    """
    Main function for the discotify command line interface.
    """
    
    parser = argparse.ArgumentParser(
        description="Discotify - A Python package and shell cli for sending text/notifications to discord"
    )
    
    parser.add_argument(
        "message",
        nargs=argparse.REMAINDER,
        help="Message to send to discord (all remaining arguments)"
    )
    
    parser.add_argument(
        "--tag",
        nargs=1,
        metavar=("tag"),
        default=None,
        help="Tag infront of the message. [TAG]"
    )
    
    parser.add_argument(
        "--username",
        nargs=1,
        metavar=("username"),
        default=None,
        help="Name of the Bot sending the message"
    )
    
    parser.add_argument(
        "--mention",
        nargs=1,
        metavar=("alias/user_id"),
        default=None,
        help="Tag a person so he receives a notification for the message. Can be comma separated list."
    )
    
    parser.add_argument(
        "--channel",
        nargs=1,
        metavar=("alias/hook_url"),
        default=None,
        help="The webhook url to send the message to. Can be comma separated list."
    )
    
    parser.add_argument(
        "--user_add",
        nargs=2,
        metavar=("alias", "user_id"),
        help="Add an alias for user_id"
    )
    
    parser.add_argument(
        "--user_remove",
        nargs=1,
        metavar=("alias/user_id"),
        help="Remove by alias or by user_id"
    )
    
    parser.add_argument(
        "--user_list",
        action="store_true",
        help="List all user_id aliases"
    )
    
    parser.add_argument(
        "--hook_add",
        nargs=2,
        metavar=("alias", "hook_url"),
        help="Add an alias for hook_url"
    )
    
    parser.add_argument(
        "--hook_remove",
        nargs=1,
        metavar=("alias/hook_url"),
        help="Remove by alias or by hook_url"
    )
    
    parser.add_argument(
        "--hook_list",
        action="store_true",
        help="List all hook_url aliases"
    )
    
    args = parser.parse_args()
    
    is_send = False
    if (not args.user_list and
        not args.hook_list and
        args.user_add is None and
        args.user_remove is None and
        args.hook_add is None and
        args.hook_remove is None):
        is_send = True
    #end
    
    if is_send is False and args.message:
        print('You cannot send message while calling --user* --hook* commands!')
        return 0
    #end
    
    dis = Discotify()
    
    if args.user_list:
        alias = dis.get_users_alias()
        print(f'User List: {"" if alias else "(none)"}')
        for key in alias:
            print(f'discotify --user_add {key} {alias[key]}')
    #end
    
    if args.hook_list:
        alias = dis.get_hooks_alias()
        print(f'Hook List: {"" if alias else "(none)"}')
        for key in alias:
            print(f'discotify --hook_add {key} {alias[key]}')
    #end
    
    if args.user_add:
        dis.user_add(args.user_add[0], args.user_add[1])
    #end
    
    if args.hook_add:
        dis.hook_add(args.hook_add[0], args.hook_add[1])
    #end
    
    if args.user_remove:
        dis.user_remove(alias=args.user_remove[0], user_id=args.user_remove[0])
    #end
    
    if args.hook_remove:
        dis.hook_remove(alias=args.hook_remove[0], hook_url=args.hook_remove[0])
    #end
    
    if is_send:
        try:
            dis.send(
                text=' '.join(args.message),
                tag=args.tag[0] if args.tag else None,
                mentions=args.mention[0].split(',') if args.mention else None,
                channels=args.channel[0].split(',') if args.channel else None
                )
        except Exception as e:
            print(e)
            return 1
    
    return 0
#end


if __name__ == "__main__":
    sys.exit(main())
#end
