# GenericHelper.py

import os
import math
import nextcord.ext.commands
from datetime import timedelta
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Convert the DEBUG variable in the .env to a bool
if os.getenv("DEBUG").upper() == 'TRUE':
    DEBUG = True
else:
    DEBUG = False


def log_command(command_name: str, ctx: nextcord.ext.commands.Context) -> None:
    """
        If DEBUG is True, prints a user's command to the console.
    :param command_name:    The name of the command being logged: str
    :param ctx:             The Context the command is being called from
    :return:                None
    """
    if DEBUG:
        print(f'{datetime.now()} - {ctx.message.author} issued command {command_name}')


def raw_seconds_to_time_str(raw_seconds: float) -> str:
    """
        Convert a raw 'ssss' integer to a 'hh:mm:ss.ms' string for readability
    :param raw_seconds:     The unformatted number of seconds to format: float
    :return:                A string formatted as 'hh:mm:ss.ms'
    """
    td = str(timedelta(seconds=raw_seconds))
    while True:
        if td == '0':
            return td
        if td[0] == '0' or td[0] == ':':
            td = td[1:]
        else:
            return td


def time_str_to_raw_seconds(time_str: str) -> float or None:
    """
        Unformat a 'hh:mm:ss.ms' string into an internal ssss float
    :param time_str:        The formatted input to convert: str
    :return:                A floating point seconds value
    """
    factor = 1
    raw_seconds = 0
    ms = 0
    pieced_str = list(reversed(time_str.split(':')))  # pieced_str = ['ms', 'ss', 'mm', 'hh']
    time_pieces = [t for t in pieced_str if t != '']  # protects against ':ss' input

    # If the seconds piece has a '.', get the milliseconds out of it
    if '.' in pieced_str[0]:
        ms, ss = math.modf(float(time_pieces[0]))
        ms = round(ms, 2)
        time_pieces[0] = ss

    # If the input is more than 'hh:mm:ss', reject it.
    if len(time_pieces) > 3:
        return None

    try:
        for piece in time_pieces:
            raw_seconds = raw_seconds + (factor * int(piece))
            factor = factor * 60
    except ValueError:
        return None
    return raw_seconds + ms
