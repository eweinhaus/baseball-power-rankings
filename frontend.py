import dash
from dash import dcc
from dash import html
import pandas as pd
import ipdb
import constants

num_sims = str(constants.NUM_SIMULATIONS)

def create_layout():
    return html.Div([
        html.Div(id="go", style={'display': 'none'}),
        dcc.Store(id = "game_results_JSON"),
        dcc.Store(id = "future_games_JSON"),
        dcc.Store(id = "standings_JSON"),
        dcc.Store(id = "adj_standings_JSON"),
        dcc.Store(id = "power_rank_JSON"),

        html.Div (
            className = "table_holder_top",
            children = [
                html.H1("Boston MABL Playoff Predictor")
            ]
        ),

        html.Div(
            className = "table_holder_1",
            children = [
                html.H2("Standings"),
                html.Table(id="standings_table")
            ]
        ),
        html.Div(
            className = "table_holder_2",
            children = [
                html.H2("Power Rankings"),
                dcc.Loading(
                    id="loading-1",
                    type="default",  # or 'graph', 'cube', 'circle', 'dot', or 'default'
                    fullscreen=False,  # Set to True to make the loading component take up the whole screen
                    children=[
                        html.Div(id="power_rank_graph_loader")
                    ],
                    className="custom-loading",
                    style={'position': 'absolute', 'left': '50%', 'top': '100px'},  # Center the loading component
                ),
            ]
        ),
        html.Div(
            className = "table_holder_3",
            children = [
                html.H2("Single Game Win Probability"),
                html.Div(
                    id = "dropdown_title_left",
                    className = "dropdown_titles", 
                    children = [
                        html.H3("Away Team"),
                    ]
                ),
                html.Div(
                    id = "dropdown_title_right", 
                    className = "dropdown_titles",
                    children = [
                        html.H3("Home Team"),
                    ]
                ),
                html.Div(
                    id = "dropdown_holder",
                    children = [
                        dcc.Dropdown(
                            id='away_team_dropdown',
                            ),
                        dcc.Dropdown(
                            id='home_team_dropdown',
                        ),
                    ]
                ),
                html.Div(
                    id = "win_prob_left",
                    className = "win_prob_holders",
                    children = [
                        html.H2(id='away_win_prob'),
                    ]
                ),
                html.Div(
                    id = "win_prob_right",
                    className = "win_prob_holders",
                    children = [
                        html.H2(id='home_win_prob'),
                    ]
                ),
            ]
        ),
        html.Div(
            className="table_holder_4",
            children=[
                html.H2("Playoff Probability"),
                dcc.Loading(
                    id="loading-2",
                    type="default",  # or 'graph', 'cube', 'circle', 'dot', or 'default'
                    fullscreen=False,  # Set to True to make the loading component take up the whole screen
                    children=[
                        html.Div(
                            id="playoff_graph_loader"
                            # Children will be dynamically updated content
                        )
                    ],
                    className="custom-loading",
                    style={'position': 'absolute', 'left': '50%', 'top': '75px'},  # Center the loading component
                ),
                html.Div(
                    id = "loading_message",
                    style={'margin-top': '175px', 'margin-bottom': '25px'},  # Center the loading component
                    children=[
                        html.H3("Simulating remainder of season "+ num_sims +" times. This may take a minute..."),
                    ]
                ),
            ]
        ),
    ])