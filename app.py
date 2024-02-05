import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import ipdb
import os

import frontend as fe
import webcrawler as wc
import data as dt
import constants
import visualizations as viz
import simulator as sim

port = int(os.environ.get("PORT", 10000))

# Initialize app and layout
app = dash.Dash(__name__)
app.layout = fe.create_layout()

# Initial callback to get all game results
@app.callback(
    Output("game_results_JSON", "data"),
    Output("future_games_JSON", "data"),
    Input("go", "children"),
)
def get_game_results(go):
    print("Running Dash App")
    #Get list of all game results
    url = constants.WEB_URL
    all_games_list = wc.get_game_outcome_list(url)

    #Create game_results and future_games dataframes and create json
    game_results_df, future_games_df = dt.get_game_results_df(all_games_list)
    game_results_JSON = game_results_df.to_json()
    future_games_JSON = future_games_df.to_json()

    return game_results_JSON, future_games_JSON

@app.callback(
    Output("standings_table", "children"),
    Output("standings_JSON", "data"),
    Input("game_results_JSON", "data"),
    prevent_initial_call = True,
)
def create_standings(game_results_JSON):
    print("Reached Creating Standings")    
    #Convert game results to df
    game_results_df = pd.read_json(game_results_JSON)

    #Create standings df
    standings_df = dt.get_standings(game_results_df)
    
    #Create standings table and JSON
    standings_table = viz.create_standings_table(standings_df)
    standings_JSON = standings_df.to_json()


    return standings_table, standings_JSON

@app.callback(
    Output("power_rank_graph_loader", "children"),
    Output("power_rank_JSON", "data"),
    Input("standings_JSON", "data"),
    Input("game_results_JSON", "data"),
    prevent_initial_call = True,
)
def create_power_rank(standings_JSON, game_results_JSON):
    print("Reached Creating Power Rank")
    if standings_JSON is None or game_results_JSON is None:
        print("Preventing Update from create_power_rank")
        if standings_JSON is None:
            print("standings_JSON is None")
        if game_results_JSON is None:
            print("game_results_JSON is None")
        raise dash.exceptions.PreventUpdate

    #Convert JSONs to dfs
    standings_df = pd.read_json(standings_JSON)
    game_results_df = pd.read_json(game_results_JSON)

    #Get pythagorean wins
    power_rank_df = dt.get_pythagorean_wins_df(standings_df)

    #Get strength of schedule
    power_rank_df = dt.get_sos(game_results_df, power_rank_df)

    #Get power ranking
    power_rank_df = dt.get_power_rank(power_rank_df, game_results_df)

    #Create pythagorean wins and JSON
    power_rank_graph = viz.create_power_rank_graph(power_rank_df)
    power_rank_JSON = power_rank_df.to_json()

    print("Reached end of create_power_rank")

    return dcc.Graph(
        id='power_rank_graph',
        figure=power_rank_graph,
        config={
            'displayModeBar': False,  # Hides the mode bar
            'staticPlot': False,  # Allows hover effects but prevents zooming
        },
        style={'height': '33vh', 'margin-top': '1vh', 'margin-bottom': '1vh', 'margin-left': '1vw', 'margin-right': '1vw'}
    ), power_rank_JSON


@app.callback(
    Output("playoff_graph_loader", "children"),
    Input("future_games_JSON", "data"),
    Input("standings_JSON", "data"),
    Input("power_rank_JSON", "data"),
    prevent_initial_call = True,
)
def create_playoff_prob(future_games_JSON, standings_JSON, power_rank_JSON):
    print("Reached Creating Playoff Prob")
    if future_games_JSON is None or standings_JSON is None or power_rank_JSON is None:
        print("Preventing Update from create_playoff_prob")
        if future_games_JSON is None:
            print("future_games_JSON is None")
        if standings_JSON is None:
            print("standings_JSON is None")
        if power_rank_JSON is None:
            print("power_rank_JSON is None")
        raise dash.exceptions.PreventUpdate
    
    #Convert JSONs to dfs
    future_games_df = pd.read_json(future_games_JSON)
    standings_df = pd.read_json(standings_JSON)
    power_rank_df = pd.read_json(power_rank_JSON)


    #Get future game probabilities
    future_prob_df = dt.get_future_game_prob(future_games_df, power_rank_df)
    
    
    #Simulate rest of season
    playoff_prob_df = sim.sim_remaining_games(standings_df, future_prob_df)
    print(playoff_prob_df)

    #Create playoff probability table
    playoff_prob_table = viz.create_playoff_graph(playoff_prob_df)

    print("Reached end of create_playoff_prob")

    return dcc.Graph(
        id='playoff_prob_graph',
        figure=playoff_prob_table,
        config={
            'displayModeBar': False,  # Hides the mode bar
            'staticPlot': False,  # Allows hover effects but prevents zooming
        },
        style={'height': '33vh', 'margin-top': '1vh', 'margin-bottom': '1vh', 'margin-left': '1vw', 'margin-right': '1vw'}
    ),


@app.callback(
    Output("away_team_dropdown", "options"),
    Output("home_team_dropdown", "options"),
    Input("power_rank_JSON", "data"),
)
def create_team_dropdowns(power_rank_JSON):
    print("Reached Creating Team Dropdowns")
    
    #Convert JSON to df
    power_rank_df = pd.read_json(power_rank_JSON)

    #Create team dropdown options
    team_dropdown_options = dt.get_team_dropdowns(power_rank_df)

    print("Reached end of create_team_dropdowns")

    return team_dropdown_options, team_dropdown_options

@app.callback(
    Output("away_win_prob", "children"),
    Output("home_win_prob", "children"),
    Input("away_team_dropdown", "value"),
    Input("home_team_dropdown", "value"),
    Input("power_rank_JSON", "data"),
    prevent_initial_call = True,
)
def get_game_prob(away_power_rank, home_power_rank, power_rank_JSON):
    print("Reached Getting Game Prob")
    if away_power_rank is None or home_power_rank is None or power_rank_JSON is None:
        print("Preventing Update from get_game_prob")
        if away_power_rank is None:
            print("away_team is None")
        if home_power_rank is None:
            print("home_team is None")
        if power_rank_JSON is None:
            print("power_rank_JSON is None")
        return None, None
    
    #Convert JSON to df
    power_rank_df = pd.read_json(power_rank_JSON)

    #Get single game win probability
    away_win_prob, home_win_prob = dt.get_single_game_win_prob(away_power_rank, home_power_rank)

    print("Reached end of get_game_prob")

    return "{:.1f}%".format(away_win_prob * 100), "{:.1f}%".format(home_win_prob * 100)





# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=port)
