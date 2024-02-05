import dash
from dash import dcc
from dash import html
import pandas as pd
import ipdb

def create_layout():
    return html.Div([
        html.Div(id="go", style={'display': 'none'}),
        dcc.Store(id = "game_results_JSON"),
        dcc.Store(id = "future_games_JSON"),
        dcc.Store(id = "standings_JSON"),
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
                html.H2("Single Game Outcome Predictor"),
                html.H3("Coming Soon", style={'text-align': 'center', 'margin-top': '50px'})
                # dcc.Dropdown(
                #     id='away_team_dropdown',
                #     options=[
                #         {'label': 'Team 1', 'value': 'Team 1'},
                #         {'label': 'Team 2', 'value': 'Team 2'},
                #         {'label': 'Team 3', 'value': 'Team 3'}
                #     ],
                #     value='Team 1'
                # ),
                # dcc.Dropdown(
                #     id='home_team_dropdown',
                #     options=[
                #         {'label': 'Team 1', 'value': 'Team 1'},
                #         {'label': 'Team 2', 'value': 'Team 2'},
                #         {'label': 'Team 3', 'value': 'Team 3'}
                #     ],
                #     value='Team 2'
                # ),
                # html.H2("Home Win Probability:"),
                # html.H2(id='home_win_prob'),
                # html.H2("Away Win Probability:"),
                # html.H2(id='away_win_prob'),

            ]
        ),
        html.Div(
            className = "table_holder_4",
            children = [
                html.H2("Playoff Probability"),
                dcc.Loading(
                    id="loading-2",
                    type="default",  # or 'graph', 'cube', 'circle', 'dot', or 'default'
                    fullscreen=False,  # Set to True to make the loading component take up the whole screen
                    children=[
                        html.Div(id="playoff_graph_loader")
                    ],
                    className="custom-loading",
                    style={'position': 'absolute', 'left': '50%', 'top': '100px'},  # Center the loading component
                )
            ]
        ),
    ])