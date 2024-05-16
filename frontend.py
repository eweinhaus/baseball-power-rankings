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
                html.H1("BMBL Playoff Predictor"),
                html.Ul([
                    html.Li(html.A("Overview", href="#overview")),
                    html.Li(html.A("Standings", href="#standings")),
                    html.Li(html.A("Power Rankings", href="#power-rankings")),
                    html.Li(html.A("Single Game Win Probability", href="#win-probability")),
                    html.Li(html.A("Playoff Probability", href="#playoff-probability")),
                ])
            ]
        ),

        html.Div(id="overview", className="section", children=[
            html.H2("Overview"),
            html.Div(className="content", children=[
                html.Img(src="/assets/BMBL_Logo.png", className="left"),
                html.Div(className="right", children=[
                    html.P([
                        "This Dash app is a live updating tool that predicts the playoff chances of each team in the Boston Metro Baseball League. ",
                        "The app crawls the league website to get the results of all games played so far this season. ",
                        "It then uses these results to calculate the current standings and power rankings of each team. ",
                        "From there it creates a Monte Carlo simulation to simulate the remainder of the season a specified number of times. ",
                        "The app then calculates the playoff chances of each team based on the results of the simulations. ",
                        html.A("See more here", href="https://github.com/eweinhaus/baseball-power-rankings/blob/main/README.md", target="_blank"),
                        "."
                    ])
                ])
            ])
        ]),

        html.Div(id="standings", className="section", children=[
            html.H2("Standings"),
            html.Div(className="content", children=[
                html.Div([
                    html.Table(id="standings_table"),
                ], className="left"),
                html.Div(className="right", children=[
                    html.P("This page uses a webcrawler to grab outcome of each game from the league website and create live league standings, updated to the minute.")
                ])
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
                html.Div(className="right", children=[
                    html.P("The power rankings page takes each team's performance thus far (Runs Scored, Runs Allowed, and Games Played) and applies Bill James' Pythagorean Win Probability formula to estimate each team's expected win percentage vs. a league average team. It then uses a derivative of Tangotigers win probability forumla, factors in each team's home field advantage and strength of schedule into pythagorean win percentage in order to get adjusted expected winning percentage, or 'Power Rank'.")
                ])
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
                html.Div(className="right", children=[
                    html.P("This page applies Tangotiger's win probability formula to each team's power rank in order to estimate the percentage chance any given home team beats any given away team in a potential matchup. It utilizes Dash callbacks in order to allow user to input any potential matchup and estimate outcome in real time.")
                ])
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
                html.Div(className="right", children=[
                    html.P("Given current standings, power rankings, individual matchup win probability, and remaining schedule, app uses Pandas and Numpy to run a Monte Carlo simulation to simulate the rest of the season 1000 times and graphs the probability that each team finishes top 6 in the standings in order to make the league playoffs.")
                ])
            ])
        ]),
    ])

app = dash.Dash(__name__)
app.layout = create_layout()

if __name__ == "__main__":
    app.run_server(debug=True)
