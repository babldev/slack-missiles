import base64
import json
import platform
import re
import socket
import sys
import time
import urllib2

from flask import Flask, request
import requests
import usb.core
import usb.util

import settings


# Protocol command bytes
DOWN = 0x01
UP = 0x02
LEFT = 0x04
RIGHT = 0x08
FIRE = 0x10
STOP = 0x20

DEVICE = None
DEVICE_TYPE = None


def setup_usb():
    # Tested only with the Cheeky Dream Thunder
    # and original USB Launcher
    global DEVICE
    global DEVICE_TYPE

    DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if DEVICE is None:
        DEVICE = usb.core.find(idVendor=0x0a81, idProduct=0x0701)
        if DEVICE is None:
            raise ValueError('Missile device not found')
        else:
            DEVICE_TYPE = "Original"
    else:
        DEVICE_TYPE = "Thunder"

    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
        try:
            DEVICE.detach_kernel_driver(0)
        except Exception, e:
            pass  # already unregistered

    DEVICE.set_configuration()


def send_cmd(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(
            0x21, 0x09, 0, 0, [0x02, cmd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    elif "Original" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])


def send_move(cmd, duration_ms):
    send_cmd(cmd)
    time.sleep(duration_ms / 1000.0)
    send_cmd(STOP)


def shoot(count=0):
    # Stabilize prior to the shot, then allow for reload time after.
    time.sleep(0.5)
    for i in range(int(count)):
        send_cmd(FIRE)
        time.sleep(4.5)


def run_command(command, value):
    command = command.lower()
    if command == 'right':
        send_move(RIGHT, value)
    elif command == 'left':
        send_move(LEFT, value)
    elif command == 'up':
        send_move(UP, value)
    elif command == 'down':
        send_move(DOWN, value)
    elif command == 'zero' or command == 'park' or command == 'reset':
        # Move to bottom-left
        send_move(DOWN, 2000)
        send_move(LEFT, 8000)
    elif command == 'pause' or command == 'sleep':
        time.sleep(value / 1000.0)
    elif command == 'fire' or command == 'shoot':
        if value < 1 or value > 4:
            value = 1
        shoot(value)
    else:
        return False

    return True


def run_command_set(command, shoot=1):
    run_command('right', command[0])
    run_command('up', command[1])

    for i in range(0, shoot):
        print 'Shoot!'
        run_command('shoot', 0)

    # Pause for calibration
    run_command('pause', command[0])

    # Zero out for next shot
    run_command('down', command[1] + 1000)
    run_command('left', command[0] + 1000)


def alert_launch(sender, target):
    message = '@{target}: MISSILE LAUNCH DETECTED! Sent from @{sender}'.format(
        target=target,
        sender=sender,
    )
    url = 'https://lyft.slack.com/services/hooks/slackbot?token={token}&channel=%23{room}'.format(
        token=settings.SLACKBOT_REMOTE_CONTROL_TOKEN,
        room=settings.SLACKBOT_REMOTE_CONTROL_ROOM,
    )
    print url
    data = requests.post(url, data=message)


app = Flask(__name__)


@app.route('/slack', methods=['POST'])
def slack():
    setup_usb()

    text = request.form['text'].lower()
    sender = request.form['user_name'].lower()
    args = text.split(' ')

    # strip the '@' from the command if it is the first char.
    cmd = args[0]
    if len(cmd) > 2 and cmd[0] == '@':
        cmd = cmd[1:]

    if cmd in settings.TARGETS:
        alert_launch(sender=sender, target=cmd)
        run_command_set(settings.TARGETS[cmd])
        return 'TARGET ACQUIRED: @{}!'.format(cmd)

    duration = 0
    if len(args) >= 2:
        duration = float(args[1])

    if run_command(cmd, duration):
        return 'RUNNING {} {}'.format(cmd, duration)
    else:
        return 'UNKNOWN COMMAND'


if __name__ == '__main__':
    app.run(debug=True)
