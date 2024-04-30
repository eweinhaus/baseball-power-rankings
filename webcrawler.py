import requests
from bs4 import BeautifulSoup
import ipdb

def get_game_outcome_list(url):
    #Get data from website
    response = requests.get(url)
    webpage_text = BeautifulSoup(response.content, 'html.parser')
    
    #Get list of all games that haven't been played yet
    future_games = []
    for tr in webpage_text.find_all('tr'):
        if len(tr.find_all('td')) >= 5: # Check if the 'tr' contains at least 5 'td's
            td = tr.find_all('td')[4]  # Get the 5th 'td' (index starts from 0)
            # Check if the 'td' does not contain an 'a' tag and contains "@"
            if not td.find('a') and "@" in td.get_text(strip=True):
                try:
                    new_game = td.get_text(strip=True).split("(")[0] + td.get_text(strip=True).split(")")[1]
                except:
                    new_game = td.get_text(strip=True)
                future_games.append(new_game.strip())

    ipdb.set_trace()
    #Get list of all finished games and scores
    a_tags = webpage_text.find_all('a')
    links_text_full = [a.get_text() for a in a_tags]
    game_results = [item for item in links_text_full if "@" in item]

    all_games = future_games + game_results


    return all_games

