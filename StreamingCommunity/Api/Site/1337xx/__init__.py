# 02.07.24

from urllib.parse import quote_plus


# External library
from rich.console import Console
from rich.prompt import Prompt


# Internal utilities
from StreamingCommunity.Api.Template import get_select_title
from StreamingCommunity.Api.Template.config_loader import site_constant
from StreamingCommunity.Api.Template.Class.SearchType import MediaItem


# Logic class
from .site import title_search, media_search_manager, table_show_manager
from .title import download_title


# Variable
indice = 3
_useFor = "film_serie"
_deprecate = False
_priority = 2
_engineDownload = "tor"

console = Console()
msg = Prompt()



def process_search_result(select_title):
    """
    Handles the search result and initiates the download for either a film or series.
    """
    download_title(select_title)

def search(string_to_search: str = None, get_onlyDatabase: bool = False, direct_item: dict = None):
    """
    Main function of the application for search film, series and anime.

    Parameters:
        string_to_search (str, optional): String to search for
        get_onylDatabase (bool, optional): If True, return only the database object
        direct_item (dict, optional): Direct item to process (bypass search)
    """
    if direct_item:
        select_title = MediaItem(**direct_item)
        process_search_result(select_title)
        return

    if string_to_search is None:
        string_to_search = msg.ask(f"\n[purple]Insert word to search in [green]{site_constant.SITE_NAME}").strip()

    # Perform the database search
    len_database = title_search(quote_plus(string_to_search))

    # If only the database is needed, return the manager
    if get_onlyDatabase:
        return media_search_manager

    if len_database > 0:
        select_title = get_select_title(table_show_manager, media_search_manager)
        download_title(select_title)

    else:

        # If no results are found, ask again
        console.print(f"\n[red]Nothing matching was found for[white]: [purple]{string_to_search}")
        search()