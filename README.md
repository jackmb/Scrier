# Scrier
Discord bot that announces a user's joining a channel with a user-specified audio clip

Scrier is an overhaul / rework of a proof-of-concept Discord bot I wrote a while back. The original ("IntroBot") was much clunkier to use, had less readable code, was instable.
Most importantly, IntroBot used the now-defunct discord.py libary. All of the above shortcomings have been corrected by Scrier, which now uses nextcord.

-----------------------------------------------

REQUIREMENTS
  - FFMpeg
  - nextcord
  - yt_dlp
  
Included in Python's Standard Library
  - asyncio
  - math
  - os
  - pickle
  - re
  - time
  - urllib
  
-----------------------------------------------
  
FEATURES
  - Save YouTube videos alongside a start-time and clip duration
  - Search YouTube for your intro video
  - Play the YouTube video clip when joining a Discord voice channel
  - Return details of your specified intro

-----------------------------------------------

KNOWN ISSUES
  - None yet. If you find one, please submit an issue.
  
-----------------------------------------------

TO-DO LIST
  - Add 'invite' command that gives a link anyone can use to invite the bot to new servers.
    Invite link should be specified in .env.
  - Intro "queueing", so if a user joins while another user's intro is playing, the second's intro is played right after.
  - Store intro info (link, start time, duration) in a SQL database instead of pickles.
  - Add support for nextcord slash commands.
  - Allow users to send their own .mp3 or .wav files
