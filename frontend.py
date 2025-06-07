import dash
from dash import dcc
from dash import html
import pandas as pd
import constants

num_sims = str(constants.NUM_SIMULATIONS)

def create_layout():
    return html.Div([
        html.Div(id="go", style={'display': 'none'}),
        dcc.Store(id="game_results_JSON"),
        dcc.Store(id="future_games_JSON"),
        dcc.Store(id="standings_JSON"),
        dcc.Store(id="adj_standings_JSON"),
        dcc.Store(id="power_rank_JSON"),

        html.Header(className="dashboard-header", children=[
            html.H1("BMBL Playoff Predictor"),
            html.Div(className="header-description", children=[
                html.P([
                    "A live updating tool used to predict the playoff chances of each team in the Boston Metro Baseball League. ",
                    html.A("See more here", href="https://github.com/eweinhaus/baseball-power-rankings/blob/main/README.md", target="_blank"),
                    "."
                ]),
            ]),
        ]),

        html.Div(className="dashboard", children=[
            # Standings Section
            html.Div(className="dashboard-section", children=[
                html.H2("Standings"),
                html.Table(id="standings_table"),
            ]),

            # Power Rankings Section
            html.Div(className="dashboard-section", children=[
                html.H2("Power Rankings"),
                dcc.Loading(
                    id="loading-1",
                    type="default",
                    children=html.Div(id="power_rank_graph_loader"),
                    className="custom-loading"
                ),
            ]),

            # Win Probability Section
            html.Div(className="dashboard-section", children=[
                html.H2("Single Game Win Probability"),
                html.Div(className="dropdown-holder", children=[
                    html.Div(className="dropdown", children=[
                        html.H3("Away Team"),
                        dcc.Dropdown(id='away_team_dropdown'),
                    ]),
                    html.Div(className="dropdown", children=[
                        html.H3("Home Team"),
                        dcc.Dropdown(id='home_team_dropdown'),
                    ]),
                ]),
                html.Div(className="win-prob-holder", children=[
                    html.Div(id='away_win_prob', className="win-prob"),
                    html.Div(id='home_win_prob', className="win-prob"),
                ]),
            ]),

            # Playoff Probability Section
            html.Div(className="dashboard-section", children=[
                html.H2("Playoff Probability"),
                dcc.Loading(
                    id="loading-2",
                    type="default",
                    children=html.Div(id="playoff_graph_loader"),
                    className="custom-loading"
                ),
                html.Div(id="loading_message", children=[
                    html.H4(f"Simulating remainder of season {num_sims} times. This may take a minute..."),
                ]),
            ]),
        ]),
    ])

app = dash.Dash(__name__)
app.layout = create_layout()

if __name__ == "__main__":
    app.run_server(debug=False)
