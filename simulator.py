import pandas as pd
import random
from collections import defaultdict
import constants
import ipdb

def sim_one_season(standings_dict, future_prob_df):
    # Simulate a season using dictionaries for faster updates
    sim_standings = standings_dict.copy()

    for index, row in future_prob_df.iterrows():
        winner = row["HomeTeam"] if random.random() < row["HomeWinPct"] else row["AwayTeam"]
        sim_standings[winner] += 2

    # Custom sort function to handle tiebreakers
    sorted_teams = sorted(sim_standings, key=lambda x: (sim_standings[x], random.random()), reverse=True)
    
    return sorted_teams[:constants.NUM_PLAYOFF_TEAMS]

def sim_remaining_games(standings_df, future_prob_df):
    # Convert standings DataFrame to a dictionary for faster access
    standings_dict = dict(zip(standings_df["Team"], standings_df["Points"]))
    
    # Initialize the outcomes dictionary
    outcomes_dict = defaultdict(int)

    # Simulate seasons
    for i in range(constants.NUM_SIMULATIONS):
        if i % 100 == 0:
            print("Simulating season", i + 1, "of", constants.NUM_SIMULATIONS)
        playoff_teams = sim_one_season(standings_dict, future_prob_df)
        for team in playoff_teams:
            outcomes_dict[team] += 1

    print("Simulation complete")

    # Convert outcomes to DataFrame
    outcomes_df = pd.DataFrame({'Team': list(outcomes_dict.keys()), 
                                'Made Playoffs': list(outcomes_dict.values())})
    outcomes_df['Playoff Probability'] = outcomes_df['Made Playoffs'] / constants.NUM_SIMULATIONS
    outcomes_df = outcomes_df.sort_values(by='Playoff Probability', ascending=False)
    
    
    #include teams that made playoffs zero times
    for team in standings_dict:
        if team not in outcomes_df["Team"].values:
            new_row = {"Team": team, "Made Playoffs": 0, "Playoff Probability": 0}
            outcomes_df = pd.concat([outcomes_df, pd.DataFrame([new_row])], ignore_index=True)

            
    return outcomes_df
