import argparse
from sys import argv

import __init__ as main

# Parse command line arguments if running standalone
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
        spesdebris: PC automation and cross-device communication suite
        """
    )
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_upload = subparsers.add_parser(
        "upload",
        help='Upload the specified file to your Android device'
    )
    parser_upload.add_argument('source_file', type=str)
    parser_upload.add_argument('-destination', type=str)
    parser_upload.set_defaults(func=main.upload_to_phone)

    parser_daemon = subparsers.add_parser(
        "daemon",
        help='Run spesdebris as a background process'
    )
    parser_daemon.set_defaults(func=main.daemon_mode)

    parser_fcm_send = subparsers.add_parser(
        "fcm_send",
        help="Send FCM message"
    )
    parser_fcm_send.add_argument('message', type=str)
    parser_fcm_send.set_defaults(func=main.send_fcm_message)

    args = parser.parse_args()

    if len(argv) > 1:
        args.func(args)
    else:
        parser.parse_args("--help".split())
