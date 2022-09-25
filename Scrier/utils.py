# Utils.py

import math
import nextcord
import ast
import pickle

import youtube_dl
import asyncio
import random

from configparser import ConfigParser
from os.path import exists


class ConfigUtil:
    """
        Config Utility functions for intro bot
    """
    def __init__(self):
        self.invalid_config_message = """Config file is invalid
        likely due to a missing starting guild id or an invalid invite link"""

    def get_prefix(self, client, message):
        """
            Get prefixes from config.ini
        :param client:      nextcord.Client object, automatically passed
        :param message:     nextcord.Message object
        :return:            guild prefix str from config
        """
        server_config = self.read_config('SERVER_SETTINGS')
        # in DM messages force default prefix
        return server_config[str(message.guild.id)]['prefix']

    @staticmethod
    def read_config(field):
        """
            Get server options from config.ini
            Convert to proper types here (default is str)
        :param field:   config.ini field to read and return values from
        :return:        Tuple with config values
        """
        config_object = ConfigParser()
        config_object.read("config.ini")
        config_field = config_object[field]

        config_dict = {}
        if field == 'BOT_SETTINGS':
            config_dict["invite_link"] = str(config_field['invite_link'])
            config_dict['ydl_opts'] = ast.literal_eval(config_field['ydl_opts'])
            config_dict['ffmpeg_opts'] = ast.literal_eval(config_field['ffmpeg_opts'])
            config_dict['embed_theme'] = int(config_field['embed_theme'], 0)
            config_dict['default_prefix'] = str(config_field['default_prefix'])
            config_dict['view_timeout'] = int(config_field['view_timeout'])
            config_dict['broken'] = config_field.getboolean('broken')
        elif field == 'SERVER_SETTINGS':
            for i in config_field.keys():
                temp = ast.literal_eval(config_field[i])
                config_dict[i] = {'prefix': temp['prefix'], 'loop': bool(temp['loop'])}
        else:
            print("Bad field passed to read_config")
        return config_dict

    @staticmethod
    def write_config(mode, field, key, value=None):
        """
            Writes/Deletes key-value pair to config.ini
        :param mode:    'w' = write | 'd' = delete
        :param field:   Config.ini field
        :param key:     Key for value in config
        :param value:   Value for key in config
        :return:        None
        """
        config_object = ConfigParser()
        config_object.read("config.ini")
        config_field = config_object[str(field)]

        if mode == 'w':
            config_field[str(key)] = str(value)
        elif mode == 'd':
            config_field.pop(str(key))
        else:
            print('invalid config write mode')

        # Update config file
        with open('config.ini', 'w') as conf:
            config_object.write(conf)

    def validate_config(self):
        """
            Checks for a valid default guild id and invite link, set in config.ini
        :return: validity of config file : bool
        """
        guild_id_length = 18

        settings = self.read_config('BOT_SETTINGS')
        servers = self.read_config('SERVER_SETTINGS')

        # Check link
        link_checks = ['https://discord.com', 'oauth', 'client_id', 'bot', 'applications.commands', 'permissions=8']
        is_link_valid = True if False not in [check in settings['invite_link'] for check in link_checks] else False

        # Check start guild id
        is_guild_valid = True if len(str(list(servers.keys())[0])) == guild_id_length else False

        if is_link_valid and is_guild_valid:
            print("<><><><><><><> WhosThat is Ready <><><><><><><><>")
        else:
            print(self.invalid_config_message)
            print("Bot running in restricted mode, please update config and restart")

        return True if is_link_valid and is_guild_valid else False


class Util:
    """
        Utility functions for intro bot
    """

    def __init__(self):
        config_obj = ConfigUtil()
        config = config_obj.read_config('BOT_SETTINGS')
        self.ydl_opts = config['ydl_opts']

    @staticmethod
    def tuple_to_string(tup):
        """
            Converts an indeterminate length tuple to a string
        :return:    string
        """
        temp = ""
        for i in tup:
            temp += i + " "
        return temp.strip()

    @staticmethod
    def intro_info_to_tuple(intro_info, requester):
        """
            Extract info from song_info into song tuple
        :param intro_info:   dict from youtube_dl download
        :param requester:      string:ctx.message.author
        :return:            tuple:(string:title,
                                    string:url,
                                    string:web_page,
                                    string:ctx.message.author,
                                    int:duration,
                                    string:thumbnail)
        """
        title = intro_info['title']
        url = intro_info['formats'][0]['url']
        web_page = intro_info['webpage_url']
        duration = intro_info['duration']
        return title, url, web_page, requester, duration


    @staticmethod
    def scrub_intro_title(title):
        """
            Removes invalid characters from intro title strings
        :param title:   intro title string
        :return:        Scrubbed intro title string
        """
        return ''.join(c for c in title if (c.isalnum() or c == ' '))


def create_empty_dict():
    intro_dict = {"INITIAL_KEY": "INITIAL_VALUE"}
    pickled_dict = open_pickle('write')
    pickle.dump(intro_dict, pickled_dict)
    pickled_dict.close()


def download_from_yt(url, file_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'.\\intros\\{file_name}.mp3',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt',
        'default_search': 'auto',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return ydl_opts['outtmpl']


# Author is an author object
def add_intro(author: , intro_link: str):
    intro_dict = get_dict_from_pickle()

    file_name = str(author.guild) + '___' + str(author)
    print(f'File name: {file_name}')
    intro_loc = download_from_yt(intro_link, file_name)

    intro_dict[author.guild] = intro_link

    put_dict_in_pickle(intro_dict)

    return intro_loc


def remove_intro(user: int):
    intro_dict = get_dict_from_pickle()

    del intro_dict[user]

    put_dict_in_pickle(intro_dict)


def get_intro(user: int):
    intro_dict = get_dict_from_pickle()
    intro = 0
    if intro_dict[user]:
        intro = intro_dict[user]
    return intro


def has_intro(user: int):
    try:
        intro_dict = get_dict_from_pickle()

        has_intro_v = False
        if user in intro_dict:
            has_intro_v = True
        return has_intro_v
    except EOFError:
        return False


def initialize_pickle():
    if not exists(f'./intros/intropedia.pickle'):
        intro_dict = {"INITIAL_KEY": "INITIAL_VALUE"}
        pickled_dict = open_pickle('write')
        pickle.dump(intro_dict, pickled_dict)
        pickled_dict.close()
        return True
    return False


def open_pickle(read_write):
    rw = ''
    if read_write == 'write':
        rw = 'wb+'
    elif read_write == 'read':
        initialize_pickle()
        rw = 'rb'
    dict_dir = f'./intros/intropedia.pickle'
    return open(dict_dir, rw)


def get_dict_from_pickle():
    pickled_dict = open_pickle('read')
    ret_dict = pickle.load(pickled_dict)
    pickled_dict.close()
    return ret_dict


def put_dict_in_pickle(write_dict):
    pickled_dict = open_pickle('write')
    pickle.dump(write_dict, pickled_dict)
    pickled_dict.close()
    return


def joining_from_none(before, after):
    if before.channel is None and after.channel is not None:
        return True
    return False
