# YouTubeHelper.py

import os
import urllib.request
import re
import yt_dlp as youtube_dl
from dotenv import load_dotenv

load_dotenv()

YDL_OPTS = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'continue_dl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192', }]
    }


def keywords_to_url(search_term: str) -> str:
    """
        Given a string to use to search, find the URL of the first search result on YouTube
    :param search_term:     The search term: str
    :return:                The URL of the first search result
    """
    search_term = search_term.replace(' ', '+')
    html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={search_term}')
    videos = re.findall(r'watch\?v=(\S{11})', html.read().decode())
    return f'https://www.youtube.com/watch?v={videos[0]}'


def get_valid_yt_url(argument: str) -> (str, bool):
    """
        Given a URL or a search term, return the URL and whether it was looked up or already known
    :param argument:        The link or term to look up
    :return:                (str, bool) where str is the URL of the video and bool is whether it was searched or known.
    """
    if ('https://www.youtube.com' in argument) or ('https://youtu.be' in argument):
        return argument, False
    else:
        return keywords_to_url(argument), True


def get_yt_info(link: str) -> None or dict:
    """
        Using yt_dlp, return a YouTube video's info.
    :param link:        The URL of the YouTube video
    :return:            None if the URL is a playlist or couldn't be parsed, else the dictionary of the video's info.
    """
    ytdl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

    try:
        with ytdl:
            result = ytdl.extract_info(link, download=False)
    except youtube_dl.utils.DownloadError:
        return None

    if 'entries' in result:
        return None
    else:
        return result


def get_ffmpeg_compatible_link(link: str) -> str:
    """
        Convert a usual YouTube video URL to an ffmpeg-streamable link
    :param link:        The URL of the YouTube video
    :return:            The URL of the video's stream
    """
    aud_info = None
    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        while not aud_info:
            aud_info = ydl.extract_info(link, download=False)
            # Detect if link is a playlist
            try:
                if aud_info and aud_info['_type'] == 'playlist':
                    # If link is a playlist set song_info to a list of songs
                    aud_info = aud_info['entries']
            except KeyError:
                pass
    return aud_info['url']


def get_timestamped_link(link: str, time: int) -> str:
    """
        Append a time argument to a YouTube video URL, so clicking it begins playing at the time.
    :param link:        The URL of the YouTube video
    :param time:        The time to start playing the video when the URL is visited
    :return:            The time-modified URL
    """
    return link + '&t=' + str(time)
