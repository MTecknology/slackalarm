SlackAlarm
==========

This is a simple script that uses cron, slack, smtp, and sms as an alarm clock.
Based on check type (active,away), determine if slack status matches and, if
needed, send user a notification.


.. note::
    This currently checks based on a manually configured presence. Any presence
    change caused by automatic away checks do not seem to update this value.

Setup
-----

**Configuration**:

Create a copy of config.sample and update as needed.

**VirtualEnv**::

    python3 -m venv --prompt slackalarm ~/slackalarm/.venv
    ~/slackalarm/.venv/bin/pip3 install -r requirements.txt

Usage
-----

Examples::

    ./slackalarm.py -c .config -v /tmp/vacation
    ./slackalarm.py -c .config -v /tmp/vacation -p away
    ./slackalarm.py -c .config -v /tmp/vacation -p active

Examples
--------

Wrapper
+++++++

An example of a simple wrapper script to make cron entries a bit prettier:

``/home/user/.bin/slackalarm-wrap``::

    #!/bin/sh
   /home/user/slackalarm/.venv/bin/python3 /home/user/slackalarm/slackalarm.py -c /home/user/slackalarm/.config -v /tmp/vacation -p "$1"

Sample Cron
+++++++++++

Verbose::

    */5 8 * * 1-5 /home/user/slackalarm/.venv/bin/python3 /home/user/slackalarm/slackalarm.py -c ~/home/user/slackalarm/.config -v /tmp/vacation -p away

With Wrapper::

    30,40,50-59  8  * * 1-5 /home/user/.bin/slackalarm-wrap away
    *            9  * * 1-5 /home/user/.bin/slackalarm-wrap away
    */11        17  * * 1-5 /home/user/.bin/slackalarm-wrap active
