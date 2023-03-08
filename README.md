# Scrier

A scrier, in fantasy and folklore, is one who can see beyond the limitations of thier eyes and circumstance - often through the use of a scrying tool like a crystal ball.

This Scrier is a Discord bot that announces a user's joining a channel with that user's specified audio clip. It does this so users that are already in the channel don't need to ask "Who's that?".

Scrier is an overhaul / rework of a proof-of-concept Discord bot I wrote a while back. The original ("IntroBot") was much clunkier to use, had less readable code, and was instable.

Most importantly, IntroBot used the now-defunct discord.py libary. All of the above shortcomings have been corrected by Scrier, which now uses nextcord.

-----------------------------------------------

REQUIREMENTS
  - FFMpeg
  - nextcord
  - yt_dlp
  
Included in Python's Standard Library:
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
