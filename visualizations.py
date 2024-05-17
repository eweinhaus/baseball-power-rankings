from dash import dcc, html, dash_table
import constants
import ipdb

def create_standings_table(standings_df):
    table_df = standings_df.copy()
    # Change column names
    table_df['RF'] = table_df['RunsFor']
    table_df['RA'] = table_df['RunsAgainst']
    table_df['GP'] = table_df['GamesPlayed']
    table_df = table_df.drop(columns=['RunsFor', 'RunsAgainst', 'GamesPlayed'])

    standings_table = html.Table(
        # Header
        [html.Tr([html.Th(col) for col in table_df.columns])] +

        # Body
        [
            html.Tr([
                html.Td(table_df.iloc[i][col], className='points-column' if col == 'Points' else '') 
                for col in table_df.columns
            ]) 
            for i in range(len(table_df))
        ]
    )

    return standings_table


def create_power_rank_graph(power_rank_df):
    # Format data
    new_power_rank_df = power_rank_df.copy()
    new_power_rank_df['TeamNickname'] = new_power_rank_df['Team'].map(lambda x: x.split()[-1])
    new_power_rank_df['PowerRank'] = new_power_rank_df['Power Rank'].map(lambda x: "{:.1f}".format(x*100))

    # Define hover text
    hover_text = ['{}<br>{}'.format(team, prob) for team, prob in zip(new_power_rank_df['Team'], new_power_rank_df['PowerRank'])]

    # Define data for the graph
    data = [{
        'x': new_power_rank_df['TeamNickname'],
        'y': new_power_rank_df['PowerRank'],
        'yaxis': {'range': [0, 120]},
        'type': 'bar',
        'name': 'Power Rank',
        'text': hover_text,  # Set hover text
        'hoverinfo': 'text',  # Show only hover text
        'textposition': 'none',
        'marker': {
            'color': [constants.TEAM_COLORS[team][0] for team in new_power_rank_df['Team']],  # Apply team colors (fill color)
            'line': {
                'color': [constants.TEAM_COLORS[team][1] for team in new_power_rank_df['Team']],  # Apply border color
                'width': 6  # Border width
            }
        }
    }]

    # Define layout for the graph
    layout = {
        'yaxis': {'title': 'Power Rank', 'range': [0, 105]},
        'showlegend': False,
        'dragmode': False,  # Disable zoom by click-and-drag
        'margin': {'t': 0, 'b': 40, 'l': 50, 'r': 22.5},
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',  # Transparent plot background
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',  # Transparent paper background
    }

    # Return the figure object with layout and configuration to disable interaction
    return {'data': data, 'layout': layout}


def create_playoff_graph(playoff_prob_df):
    # Format data
    playoff_prob_df['TeamNickname'] = playoff_prob_df['Team'].map(lambda x: x.split()[-1])
    playoff_prob_df['Playoff Probability'] = playoff_prob_df['Playoff Probability'].map(lambda x: "{:.1f}%".format(x * 100))

    # Define hover text
    hover_text = ['{}<br>{}'.format(team, prob) for team, prob in zip(playoff_prob_df['Team'], playoff_prob_df['Playoff Probability'])]

    # Define data for the graph
    data = [{
        'x': playoff_prob_df['TeamNickname'],
        'y': playoff_prob_df['Playoff Probability'],
        'yaxis': {'range': [0, 105]},
        'type': 'bar',
        'name': 'Playoff Probability',
        'text': hover_text,  # Set hover text
        'hoverinfo': 'text',  # Show only hover text
        'textposition': 'none',
        'marker': {
            'color': [constants.TEAM_COLORS[team][0] for team in playoff_prob_df['Team']],  # Apply team colors (fill color)
            'line': {
                'color': [constants.TEAM_COLORS[team][1] for team in playoff_prob_df['Team']],  # Apply border color
                'width': 6  # Border width
            }
        }
    }]

    # Define layout for the graph
    layout = {
        'yaxis': {'title': 'Probability (%)', 'range': [0, 105]},
        'showlegend': False,
        'dragmode': False,  # Disable zoom by click-and-drag
        'margin': {'t': 0, 'b': 40, 'l': 50, 'r': 22.5},
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',  # Transparent plot background
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',  # Transparent paper background
    }

    # Return the figure object with layout and configuration to disable interaction
    return {'data': data, 'layout': layout}
