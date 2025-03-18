# 02.07.24

import sys

# External libraries
import httpx
from bs4 import BeautifulSoup
from rich.console import Console

from StreamingCommunity.TelegramHelp.telegram_bot import get_bot_instance
# Internal utilities
from StreamingCommunity.Util.config_json import config_manager
from StreamingCommunity.Util.headers import get_userAgent
from StreamingCommunity.Util.table import TVShowManager


# Logic class
from StreamingCommunity.Api.Template.config_loader import site_constant
from StreamingCommunity.Api.Template.Class.SearchType import MediaManager


# Variable
console = Console()
media_search_manager = MediaManager()
table_show_manager = TVShowManager()
max_timeout = config_manager.get_int("REQUESTS", "timeout")


def title_search(word_to_search: str) -> int:
    """
    Search for titles based on a search query.

    Parameters:
        - title_search (str): The title to search for.

    Returns:
        - int: The number of titles found.
    """
    if site_constant.TELEGRAM_BOT:
        bot = get_bot_instance()

    media_search_manager.clear()
    table_show_manager.clear()

    search_url = f"{site_constant.FULL_URL}/search/{word_to_search}/1/"
    console.print(f"[cyan]Search url: [yellow]{search_url}")

    try:
        response = httpx.get(search_url, headers={'user-agent': get_userAgent()}, timeout=max_timeout, follow_redirects=True)
        response.raise_for_status()

    except Exception as e:
        console.print(f"Site: {site_constant.SITE_NAME}, request search error: {e}")
        if site_constant.TELEGRAM_BOT:
            bot.send_message(f"ERRORE\n\nErrore nella richiesta di ricerca:\n\n{e}", None)
        return 0

    # Prepara le scelte per l'utente
    if site_constant.TELEGRAM_BOT:
        choices = []

    # Create soup and find table
    soup = BeautifulSoup(response.text, "html.parser")


    i = 0
    # non ho usato enumerate poichè vi è un try che potrebbe sfalzare gli indici.
    # lasciare così o tenerne conto se si modifica.
    for tr in soup.find_all('tr'):
        try:

            title_info = {
                'name': tr.find_all("a")[1].get_text(strip=True),
                'url': tr.find_all("a")[1].get("href"),
                'seader': tr.find_all("td")[-5].get_text(strip=True),
                'leacher': tr.find_all("td")[-4].get_text(strip=True),
                'date': tr.find_all("td")[-3].get_text(strip=True).replace("'", ""),
                'size': tr.find_all("td")[-2].get_text(strip=True),
                'type': 'torrent'
            }
            media_search_manager.add_media(title_info)

            if site_constant.TELEGRAM_BOT:
                choice_text = f"{i} - {title_info['name']} - {title_info['seader']} - ({title_info['size']})"
                choices.append(choice_text)

            i += 1

        except Exception as e:
            print(f"Error parsing a film entry: {e}")

    if site_constant.TELEGRAM_BOT:
        if choices:
            bot.send_message(f"Lista dei risultati:", choices)

    # Return the number of titles found
    return media_search_manager.get_length()