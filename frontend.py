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

        html.Nav(
            className="navbar",
            children=[
                #html.Img(src="/assets/BMBL_Logo.png", className="left"),
                html.H1("BMBL Playoff Predictor"),
                html.Ul([
                    html.Li(html.A("Overview", href="#overview")),
                    html.Li(html.A("Standings", href="#standings")),
                    html.Li(html.A("Power Rankings", href="#power-rankings")),
                    html.Li(html.A("Win Probability", href="#win-probability")),
                    html.Li(html.A("Playoff Odds", href="#playoff-probability")),
                ])
            ]
        ),


        
        html.Div(id="overview", className='overview-page', children=[
            html.H2("Overview"),
            html.Div([
                html.P([
                    "A live updating tool used to predict the playoff chances of each team in the Boston Metro Baseball League. ",
                    html.A("See more here", href="https://github.com/eweinhaus/baseball-power-rankings/blob/main/README.md", target="_blank"),
                    "."
                ]),
            ], className='overview-text'),

            html.Div([
                html.Div([
                    html.H3("Standings"),
                    html.P(["Live updated standings from the league website",])
                ], className='box', id='standings-box'),

                html.Div([
                    html.H3("Power Rankings"),
                    html.P("Showing each team's expected win probability vs. a league average team")
                ], className='box', id='power-rankings-box'),
            ], className='middle-row'),

            html.Div([
                html.Div([
                    html.H3("Win Probability"),
                    html.P("Interactive tool to predict win probablity for user specified matchups")
                ], className='box', id='win-probability-box'),

                html.Div([
                    html.H3("Playoff Odds"),
                    html.P(f"Simulates the rest of the season {num_sims} times to predict live playoff odds"),
                ], className='box', id='playoff-odds-box'),
            ], className='bottom-row')
        ]),


        html.Div(id="standings", className="section", children=[
            html.H2("Standings"),
            html.Div(className="content", children=[
                html.Div([
                    html.Table(id="standings_table"),
                ], className="box"),
            ])
        ]),

        html.Div(id="power-rankings", className="section", children=[
            html.H2("Power Rankings"),
            html.Div(className="content", children=[
                html.Div([
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=html.Div(id="power_rank_graph_loader"),
                        className="custom-loading"
                    ),
                ], className="left"),
            ])
        ]),

        html.Div(id="win-probability", className="section", children=[
            html.H2("Single Game Win Probability"),
            html.Div(className="content", children=[
                html.Div([
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
                ], className="left"),
            ])
        ]),

        html.Div(id="playoff-probability", className="section", children=[
            html.H2("Playoff Probability"),
            html.Div(className="content", children=[
                html.Div([
                    dcc.Loading(
                        id="loading-2",
                        type="default",
                        children=html.Div(id="playoff_graph_loader"),
                        className="custom-loading"
                    ),
                    html.Div(id="loading_message", children=[
                        html.H3(f"Simulating remainder of season {num_sims} times. This may take a minute..."),
                    ]),
                ], className="left"),
            ])
        ]),
    ])

app = dash.Dash(__name__)
app.layout = create_layout()

if __name__ == "__main__":
    app.run_server(debug=True)
