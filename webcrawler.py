import requests
from bs4 import BeautifulSoup
import ipdb
import pandas as pd

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


    #Get list of all finished games and scores
    a_tags = webpage_text.find_all('a')
    links_text_full = [a.get_text() for a in a_tags]
    game_results = [item for item in links_text_full if "@" in item]

    all_games = future_games + game_results


    return all_games


def get_standings(url):
    #Get data from website
    response = requests.get(url)
    webpage_text = BeautifulSoup(response.content, 'html.parser')

    #Get all font tags with <a> tags
    font_tags = webpage_text.find_all('font')

    #Create blank standings dataframe
    standings = pd.DataFrame(columns = ['Team', 'Win', 'Loss', 'Tie', 'RunsFor', 'RunsAgainst', 'GamesPlayed'])

    for i in range(13, len(font_tags)):
        if i % 8 == 5 and font_tags[i].find('a'):
            team = font_tags[i].find('a').get_text()
            win = int(font_tags[i + 1].get_text())
            loss = int(font_tags[i + 2].get_text())
            tie = int(font_tags[i + 3].get_text())
            points = win * 2 + tie
            runs_for = int(font_tags[i + 6].get_text())
            runs_against = int(font_tags[i + 7].get_text())
            games_played = sum([win, loss, tie])


            standings = standings._append({'Team': team, 'Win': win, 'Loss': loss, 'Tie': tie, 'Points': points, 'RunsFor': runs_for, 'RunsAgainst': runs_against, 'GamesPlayed': games_played}, ignore_index=True)

    return standings





