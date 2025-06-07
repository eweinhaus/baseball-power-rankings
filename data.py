import pandas as pd
import ipdb
from dash import dcc, html, dash_table
import constants

def get_game_results_df(game_results):

    extracted_data = []
    for game in game_results:
        # Splitting at '@' to separate teams
        parts = game.split('@')
        home_team, away_team = parts[1].split(',')[0], parts[0] if parts[0] != '' else parts[1].split(',')[1]

        # Extracting scores
        home_score = ''.join(filter(str.isdigit, home_team))
        away_score = ''.join(filter(str.isdigit, away_team))

        # Extracting team names
        home_team = ''.join(filter(lambda x: not x.isdigit(), home_team)).strip()
        away_team = ''.join(filter(lambda x: not x.isdigit(), away_team)).strip()

        # Adding to the extracted data list
        extracted_data.append([away_team, away_score, home_team, home_score])

    # Creating a DataFrame
    game_results_df = pd.DataFrame(extracted_data, columns=['AwayTeam', 'AwayScore', 'HomeTeam', 'HomeScore'])

    #Remove any games that have not been played yet and add to future games
    future_games_df = game_results_df[game_results_df["AwayScore"] == ""][["AwayTeam", "HomeTeam"]].reset_index(drop=True)
    game_results_df = game_results_df[game_results_df["AwayScore"] != ""]

    #END OF SEASON HARDCODE: Removes last 90 played league games and set as "upcoming games" (for active seasons, only unplayed games will be removed)
    if constants.END_OF_SEASON == True:
        future_games_df = pd.concat([future_games_df, game_results_df.tail(90)[["AwayTeam", "HomeTeam"]].reset_index(drop=True)], ignore_index=True)  
        game_results_df = game_results_df.head(-90).reset_index(drop=True)

    #PRESEASON HARDCODE: Add preseason games to game results
    if constants.PRESEASON == True:
        preseason_games = [["Greater Boston Bandits", 8, "Boston Phoenix", 16], ["Boston Phoenix", 9, "Bay State Raiders", 2]]
        preseason_df = pd.DataFrame(preseason_games, columns=['AwayTeam', 'AwayScore', 'HomeTeam', 'HomeScore'])
        game_results_df = pd.concat([preseason_df, game_results_df], ignore_index=True)

    return game_results_df, future_games_df


# Function to determine the outcome of a game for a team
def game_outcome(team_score, opponent_score):
    if team_score > opponent_score:
        return 'Win'
    elif team_score < opponent_score:
        return 'Loss'
    else:
        return 'Tie'

def get_standings(game_results_df):
    # Initialize an empty dictionary to store team standings
    standings = {}

    # Iterate through each game in the DataFrame
    for index, row in game_results_df.iterrows():
        home_team, home_score, away_team, away_score = row['HomeTeam'], row['HomeScore'], row['AwayTeam'], row['AwayScore']

        # Update standings for home team
        if home_team not in standings:
            standings[home_team] = {'Win': 0, 'Loss': 0, 'Tie': 0, 'RunsFor': 0, 'RunsAgainst': 0, 'GamesPlayed': 0}
        
        standings[home_team][game_outcome(home_score, away_score)] += 1
        standings[home_team]['RunsFor'] += home_score
        standings[home_team]['RunsAgainst'] += away_score
        standings[home_team]['GamesPlayed'] += 1

        # Update standings for away team
        if away_team not in standings:
            standings[away_team] = {'Win': 0, 'Loss': 0, 'Tie': 0, 'RunsFor': 0, 'RunsAgainst': 0, 'GamesPlayed': 0}
        
        standings[away_team][game_outcome(away_score, home_score)] += 1
        standings[away_team]['RunsFor'] += away_score
        standings[away_team]['RunsAgainst'] += home_score
        standings[away_team]['GamesPlayed'] += 1

    # Convert the standings dictionary to a DataFrame
    standings_df = pd.DataFrame.from_dict(standings, orient='index').reset_index()
    standings_df.rename(columns={'index': 'Team'}, inplace=True)

    #Create Points column (2 for win, 1 for tie)
    standings_df['Points'] = standings_df['Win'] * 2 + standings_df['Tie']

    #Sort by points with Runs For being tie breaker
    standings_df = standings_df.sort_values(by=['Points'], ascending=False)
    standings_df = standings_df.reset_index(drop=True)

    return standings_df


def get_pythagorean_wins_df(standings_df):
    run_differential_df = standings_df[['Team', 'RunsFor', 'RunsAgainst', 'GamesPlayed']]

    pythag_wins_df = calc_pythag_wins(run_differential_df)


    return pythag_wins_df

def calc_pythag_wins(run_differential_df):
    #get league average pythagorean exponent
    league_exponent = ((run_differential_df["RunsFor"].sum() + run_differential_df["RunsAgainst"].sum()) / run_differential_df["GamesPlayed"].sum()) ** constants.PYTHAG_EXPONENT
    
    #Initialize New Columns
    run_differential_df = run_differential_df.copy()
    run_differential_df["Pythagorean Win Percentage"] = None

    for index, row in run_differential_df.iterrows():
        #Get team specific exponent
        team_exponent = ((10 * league_exponent) + ((((row["RunsFor"] + row["RunsAgainst"]) / row["GamesPlayed"]) ** constants.PYTHAG_EXPONENT) * row["GamesPlayed"])) / (10 + row["GamesPlayed"])
        
        #Calculate team pythagorean percentage
        team_pythag_pct = min(constants.MAX_STRENGTH, max(constants.MIN_STRENGTH, (row["RunsFor"]**team_exponent) / ((row["RunsFor"]**team_exponent) + (row["RunsAgainst"] ** team_exponent))))

        run_differential_df.at[index, "Pythagorean Win Percentage"] = team_pythag_pct
        
    return run_differential_df


def get_sos(game_results_df, pythag_wins_df):
    
    #Create new dataframe to store strength of schedule
    sos_df = pythag_wins_df.copy()

    #Get list of all unique teams
    teams = pd.concat([game_results_df['HomeTeam'], game_results_df['AwayTeam']]).unique()

    for team in teams:
        #Get list of all previous opponents
        home_opponents = game_results_df[game_results_df['HomeTeam'] == team]["AwayTeam"]
        away_opponents = game_results_df[game_results_df['AwayTeam'] == team]["HomeTeam"]
        all_opponents = pd.concat([home_opponents, away_opponents])

        sos_list = []
        for opponent in all_opponents:
            sos_list.append(pythag_wins_df[pythag_wins_df["Team"] == opponent]["Pythagorean Win Percentage"].values[0])
        sos = sum(sos_list) / len(sos_list)


        sos_df.loc[sos_df["Team"] == team, "Strength of Schedule"] = sos

    return sos_df

def get_power_rank(power_rank_df, game_results_df):

    for index, row in power_rank_df.iterrows():

        #Get count of home and away games and calculate scheduled home field advantage
        home_games = game_results_df[game_results_df["HomeTeam"] == row["Team"]].shape[0]
        away_games = game_results_df[game_results_df["AwayTeam"] == row["Team"]].shape[0]
        hfa = ((constants.HOME_FIELD_ADVANTAGE * home_games) + ((1 - constants.HOME_FIELD_ADVANTAGE) * away_games)) / (home_games + away_games)

        #Get team estimated win % (pythag win % adjusted for strength of schedule and home field advantage)
        team_estimated_win_pct = (((row["Pythagorean Win Percentage"]*row["Strength of Schedule"]) * (1-hfa)) / (hfa - (row["Strength of Schedule"] * hfa) - (row["Pythagorean Win Percentage"] * hfa) + (row["Pythagorean Win Percentage"] * row["Strength of Schedule"])))
        
        #Regress to the mean
        if constants.REGRESS_TO_MEAN == True:
            team_true_win_pct = regress_to_mean(row, team_estimated_win_pct)
        else:
            team_true_win_pct = team_estimated_win_pct

        power_rank_df.at[index, "Power Rank"] = team_true_win_pct

    #Sort by power rank, tiebreaker is pythagorean win percentage
    power_rank_df = power_rank_df.sort_values(by=["Power Rank", "Pythagorean Win Percentage"], ascending=False)

    return power_rank_df

def regress_to_mean(row, team_estimated_win_pct):
    #Include last year power rank (default to 0.5 if team not found)
    last_year_power_rank = (constants.LAST_YEAR_POWR_RANK.get(row["Team"], 50) / 100) * constants.REGRESS_LAST_YEAR
    
    #Include games of .500 ball
    average = 0.5 * constants.REGRESS_500_GAMES
    
    #Include pythag win% adjusted for SoS and HFA
    estimated =  team_estimated_win_pct * row["GamesPlayed"] * constants.REGRESS_ESTIMATED

    #Include straight pythag win%
    pythag = row["Pythagorean Win Percentage"] * row["GamesPlayed"] * constants.REGRESS_PYTHAG

    return (average + estimated + pythag + last_year_power_rank) / (constants.REGRESS_LAST_YEAR + constants.REGRESS_500_GAMES + (row["GamesPlayed"] * (constants.REGRESS_ESTIMATED + constants.REGRESS_PYTHAG)))



def get_future_game_prob(future_games_df, power_rank_df):    
    #Iterate through games and get probability of home team winning
    for index, row in future_games_df.iterrows():
        #Get teams in game
        home_team = row["HomeTeam"]
        away_team = row["AwayTeam"]

        #Get power rank of home and away teams
        home_power_rank = power_rank_df[power_rank_df["Team"] == home_team]["Power Rank"].values[0]
        away_power_rank = power_rank_df[power_rank_df["Team"] == away_team]["Power Rank"].values[0]

        #Get single game win probability
        away_win_prob, home_win_prob = get_single_game_win_prob(away_power_rank, home_power_rank)
        
        #Add probability to "HomeWinPct" column in future games df in the same row as the game
        future_games_df.at[index, "HomeWinPct"] = home_win_prob

    return future_games_df

def get_single_game_win_prob(away_power_rank, home_power_rank):
    #Get probability of each team winning single matchup
    home_win_prob = ((home_power_rank * (1 - away_power_rank) * constants.HOME_FIELD_ADVANTAGE) / ((home_power_rank * (1 - away_power_rank) * constants.HOME_FIELD_ADVANTAGE) + ((1 - home_power_rank) * away_power_rank * (1 - constants.HOME_FIELD_ADVANTAGE))))
    away_win_prob = 1 - home_win_prob

    return away_win_prob, home_win_prob


def get_team_dropdowns(power_rank_df):
    new_power_rank_df = power_rank_df.copy()
    
    # Sort alphabetical by team name
    new_power_rank_df = new_power_rank_df.sort_values(by=["Team"], ascending=True)

    # Create dropdown options using full team name as label
    team_dropdown_options = [{'label': team, 'value': power_rank} for team, power_rank in zip(new_power_rank_df['Team'], new_power_rank_df['Power Rank'])]

    return team_dropdown_options