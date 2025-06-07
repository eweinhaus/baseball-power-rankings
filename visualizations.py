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
        ],
        className='standings-table'
    )

    return standings_table


def create_power_rank_graph(power_rank_df):
    # Format data
    new_power_rank_df = power_rank_df.copy()
    new_power_rank_df['PowerRank'] = new_power_rank_df['Power Rank'].map(lambda x: "{:.1f}".format(x*100))

    # Define hover text
    hover_text = ['{}<br>{}'.format(team, prob) for team, prob in zip(new_power_rank_df['Team'], new_power_rank_df['PowerRank'])]

    # Define data for the graph
    data = [{
        'x': new_power_rank_df['Team'],
        'y': new_power_rank_df['PowerRank'],
        'type': 'bar',
        'name': 'Power Rank',
        'text': hover_text,
        'hoverinfo': 'text',
        'textposition': 'none',
        'marker': {
            'color': [constants.TEAM_COLORS[team][0] for team in new_power_rank_df['Team']],
            'line': {
                'color': [constants.TEAM_COLORS[team][1] for team in new_power_rank_df['Team']],
                'width': 1
            }
        }
    }]

    # Define layout for the graph
    layout = {
        'yaxis': {
            'title': 'Power Rank',
            'range': [0, 105],
            'tickfont': {'size': 9},
            'titlefont': {'size': 11},
            'automargin': True
        },
        'xaxis': {
            'tickangle': -45,
            'tickfont': {'size': 9},
            'automargin': True
        },
        'showlegend': False,
        'dragmode': False,
        'margin': {'t': 5, 'b': 35, 'l': 45, 'r': 15},
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'height': 180,
        'width': '100%',
        'autosize': True
    }

    return {'data': data, 'layout': layout}


def create_playoff_graph(playoff_prob_df):
    # Format data
    playoff_prob_df['Playoff Probability'] = playoff_prob_df['Playoff Probability'].map(lambda x: "{:.1f}%".format(x * 100))

    # Define hover text
    hover_text = ['{}<br>{}'.format(team, prob) for team, prob in zip(playoff_prob_df['Team'], playoff_prob_df['Playoff Probability'])]

    # Define data for the graph
    data = [{
        'x': playoff_prob_df['Team'],
        'y': playoff_prob_df['Playoff Probability'],
        'type': 'bar',
        'name': 'Playoff Probability',
        'text': hover_text,
        'hoverinfo': 'text',
        'textposition': 'none',
        'marker': {
            'color': [constants.TEAM_COLORS[team][0] for team in playoff_prob_df['Team']],
            'line': {
                'color': [constants.TEAM_COLORS[team][1] for team in playoff_prob_df['Team']],
                'width': 1
            }
        }
    }]

    # Define layout for the graph
    layout = {
        'yaxis': {
            'title': 'Probability (%)',
            'range': [0, 105],
            'tickfont': {'size': 9},
            'titlefont': {'size': 11},
            'automargin': True
        },
        'xaxis': {
            'tickangle': -45,
            'tickfont': {'size': 9},
            'automargin': True
        },
        'showlegend': False,
        'dragmode': False,
        'margin': {'t': 5, 'b': 35, 'l': 45, 'r': 15},
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'height': 180,
        'width': '100%',
        'autosize': True
    }

    return {'data': data, 'layout': layout}
