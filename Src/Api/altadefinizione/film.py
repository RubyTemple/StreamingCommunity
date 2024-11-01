# 26.05.24

import os
import time


# Internal utilities
from Src.Util.console import console, msg
from Src.Util.os import remove_special_characters
from Src.Util.message import start_message
from Src.Util.call_stack import get_call_stack
from Src.Lib.Downloader import HLS_Downloader
from ..Template import execute_search


# Logic class
from .Player.supervideo import VideoSource
from ..Template.Class.SearchType import MediaItem


# Config
from .costant import ROOT_PATH, SITE_NAME, MOVIE_FOLDER


def download_film(select_title: MediaItem):
    """
    Downloads a film using the provided film ID, title name, and domain.

    Parameters:
        - title_name (str): The name of the film title.
        - url (str): The url of the video
    """

    # Start message and display film information
    start_message()
    console.print(f"[yellow]Download:  [red]{select_title.name} \n")

    # Set domain and media ID for the video source
    video_source = VideoSource(select_title.url)

    # Define output path
    mp4_name = remove_special_characters(select_title.name) + ".mp4"
    mp4_path = os.path.join(ROOT_PATH, SITE_NAME, MOVIE_FOLDER, remove_special_characters(select_title.name))

    # Get m3u8 master playlist
    master_playlist = video_source.get_playlist()

    # Download the film using the m3u8 playlist, and output filename
    r_proc = HLS_Downloader(m3u8_playlist = master_playlist, output_filename = os.path.join(mp4_path, mp4_name)).start()
    
    if r_proc == 404:
        time.sleep(2)

        # Re call search function
        if msg.ask("[green]Do you want to continue [white]([red]y[white])[green] or return at home[white]([red]n[white]) ", choices=['y', 'n'], default='y', show_choices=True) == "n":
            frames = get_call_stack()
            execute_search(frames[-4])

    if r_proc != None:
        console.print("[green]Result: ")
        console.print(r_proc)
