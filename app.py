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

    return dcc.Graph(
        id='playoff_prob_graph',
        figure=playoff_prob_table,
        config={
            'displayModeBar': False,  # Hides the mode bar
            'staticPlot': False,  # Allows hover effects but prevents zooming
        },
        style={'height': '33vh', 'margin-top': '1vh', 'margin-bottom': '1vh', 'margin-left': '1vw', 'margin-right': '1vw'}
    ),




# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=port)
