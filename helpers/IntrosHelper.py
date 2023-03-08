# IntrosHelper.py
# jasmine wuz here ^_^

import pickle
import os
from os.path import exists
from typing import BinaryIO
from dotenv import load_dotenv

load_dotenv()

intros_dir = os.getenv("INTROS_DIR")
duration_dir = os.getenv("DURATIONS_DIR")
start_time_dir = os.getenv("START_TIME_DIR")


def initialize_pickle(pickle_dir: str) -> bool:
    """
        Check if a pickle exists, and create it if it doesn't.
        Helps to safeguard against pickles' poor handling of missing / empty pickles.
    :param pickle_dir:      The directory of the pickle to check and initialize: str
    :return:                True if the pickle was created, else False
    """
    if not exists(pickle_dir):
        pickled_dict = open_pickle_write(pickle_dir)
        intro_dict = {'INIT_KEY': 'INIT_VAL'}
        pickle.dump(intro_dict, pickled_dict)
        pickled_dict.close()
        return True
    return False


def open_pickle_write(pickle_dir: str) -> BinaryIO:
    """
        Open a BinaryIO stream to write to
    :param pickle_dir:      The directory of the pickle to open: str
    :return:                The BinaryIO stream to write to
    """
    return open(pickle_dir, 'wb+')


def open_pickle_read(pickle_dir: str) -> BinaryIO:
    """
        Open a BinaryIO stream to read from
    :param pickle_dir:      The directory of the pickle to open: str
    :return:                The BinaryIO stream to read from
    """
    initialize_pickle(pickle_dir)  # pickles cause problems if you try to read from nonexistent ones
    return open(pickle_dir, 'rb')


def get_dict_from_pickle(pickle_dir: str) -> dict:
    """
        From a pickle, return the packed dictionary object
    :param pickle_dir:      The directory of the pickle to read: str
    :return:                The dictionary object stored in the pickle
    """
    pickled_dict = open_pickle_read(pickle_dir)
    ret_dict = pickle.load(pickled_dict)
    pickled_dict.close()
    return ret_dict


def put_dict_in_pickle(write_dict: dict, pickle_dir: str) -> None:
    """
        Save a dictionary object into a pickle file
    :param write_dict:      The dictionary object to save off. Will replace the existing pickled dictionary: dict
    :param pickle_dir:      The directory of the pickle to save the dictionary to: str
    :return:                None
    """
    pickled_dict = open_pickle_write(pickle_dir)
    pickle.dump(write_dict, pickled_dict)
    pickled_dict.close()
    return


def get_val_from_pickled_dict(pickle_dir: str, key: int) -> str or None:
    """
        Read one value from a pickled dictionary
    :param pickle_dir:      The directory of the pickle to read the value from: str
    :param key:             The key to look up in the pickled dictionary: int
    :return:                The str value if found, else None
    """
    depickled_dict = get_dict_from_pickle(pickle_dir)
    try:
        ret_val = depickled_dict[key]
    except KeyError:
        return None
    return ret_val


def set_val_in_pickled_dict(pickle_dir: str, key: int, val: str or float) -> None:
    """
        Write one value to a pickled dictionary
    :param pickle_dir:      The directory of the pickle to write the value to: str
    :param key:             The key to save to the dictionary: int
    :param val:             The value to save to the dictionary: str or float
    :return:                None
    """
    depickled_dict = get_dict_from_pickle(pickle_dir)
    depickled_dict[key] = val
    put_dict_in_pickle(depickled_dict, pickle_dir)
    return


def get_intro_tuple(user_key: int) -> (str, float, float) or None:
    """
        Given a user ID as a key, read from the three primary pickles the user's intro info and return it
    :param user_key:        The user ID used to find the info in the pickles: int
    :return:
    """
    link = get_val_from_pickled_dict(intros_dir, user_key)
    duration = get_val_from_pickled_dict(duration_dir, user_key)
    start_time = get_val_from_pickled_dict(start_time_dir, user_key)
    if (link is None) or (duration is None) or (start_time is None):
        return None
    else:
        return link, duration, start_time


def set_intro(user_key: int, link: str, duration: float, start_time: float) -> None:
    """
        Given a user ID, intro link, start time, and duration, store each away in their respective pickled dictionaries.
    :param user_key:        The user ID used to key the other three values: int
    :param link:            The YouTube link of the user's intro to store in the intropedia pickle: str
    :param duration:        The duration of the user's intro to store in the duration pickle: float
    :param start_time:      The start time of the user's intro to store in the start time pickle: float
    :return:
    """
    set_val_in_pickled_dict(intros_dir, user_key, link)
    set_val_in_pickled_dict(duration_dir, user_key, duration)
    set_val_in_pickled_dict(start_time_dir, user_key, start_time)
    return
