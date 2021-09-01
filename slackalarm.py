#!/usr/bin/env python3
'''
SlackAlarm: Check if a user is 'on-line' and prod if not available.

To the extent possible under law, the person who associated CC0 with
authors have waived all copyright and related or neighboring rights
to SlackAlarm.

You should have received a copy of the CC0 legalcode along with this
work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
'''
import argparse
import email
import os
import smtplib
import slack_sdk
import socket
import yaml


def main():
    '''
    Check & Ping
    '''
    # Read options
    parser = argparse.ArgumentParser(
            usage='slackalarm.py [-h] <optional arguments> [operation] <options>',
            formatter_class=lambda prog: argparse.HelpFormatter(
                    prog, max_help_position=30))
    parser.add_argument(
        '-p', '--ping',
        choices=['active', 'away'],
        dest='check',
        metavar='X',
        help='ping if status is {active,away} (default: away)',
        default='away')
    parser.add_argument(
        '-c', '--config',
        dest='config',
        action='store',
        metavar='X',
        help='config path (default: .config)',
        default='.config')
    parser.add_argument(
        '-v', '--vacation',
        dest='disable_path',
        action='store',
        metavar='X',
        help='if path exists, then skip checks (default /tmp/vacation)',
        default='.config')

    opts = parser.parse_args()

    # Read config
    conf = yaml.safe_load(open(opts.config, 'r'))

    # Vacation check
    if os.path.exists(opts.disable_path):
        return

    # Check status
    status = check_user(conf['bot_token'], conf['watch_user'])

    # Notify user
    if opts.check == 'away' and status != 'active':
        _notify_user(conf, 'INACTIVE ALERT: Where Are You?!')
    if opts.check == 'active' and status == 'active':
        _notify_user(conf, 'Hey, go home! (after setting away status)')


def check_user(token, uid):
    '''
    Check status of user (uid) from Web API request (token).
    Returns: ['active', 'away', None]
    '''
    client = slack_sdk.WebClient(token=token)

    try:
        resp = client.users_getPresence(user=uid)
    except slack_sdk.errors.SlackApiError as e:
        assert e.response['error']

    return resp.get('presence')


def _notify_user(conf, message):
    '''
    Send notification to user
    '''
    eml = email.message.EmailMessage()
    eml.set_content(message)
    eml['Subject'] = 'SlackAlarm Notification'
    eml['From'] = f'slackalarm@{socket.getfqdn()}'
    eml['To'] = conf['notify_addr']

    s = smtplib.SMTP(
        conf.get('smtp_host', 'smtp.gmail.com'),
        conf.get('smtp_port', 587))
    if conf.get('smtp_starttls', True):
        s.starttls()
    s.login(conf['smtp_user'], conf['smtp_pass'])
    s.send_message(eml)
    s.quit()


if __name__ == '__main__':
    main()
