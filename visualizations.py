from dash import dcc, html, dash_table
import ipdb

def create_standings_table(standings_df):
    table_df = standings_df.copy()
    #Change column names
    table_df['RF'] = table_df['RunsFor']
    table_df['RA'] = table_df['RunsAgainst']
    table_df['GP'] = table_df['GamesPlayed']
    table_df = table_df.drop(columns = ['RunsFor', 'RunsAgainst', 'GamesPlayed'])
    

    standings_table = html.Table(
        # Header
        [html.Tr([html.Th(col) for col in table_df.columns])] +

        # Body
        [html.Tr([html.Td(table_df.iloc[i][col]) for col in table_df.columns]) for i in range(len(table_df))]
    )

    return standings_table


def create_power_rank_graph(power_rank_df):
    # Format data
    power_rank_df['TeamNickname'] = power_rank_df['Team'].map(lambda x: x.split()[-1])
    power_rank_df['PowerRank'] = power_rank_df['Power Rank'].map(lambda x: "{:.1f}".format(x*100))


    # Define hover text
    hover_text = ['{}<br>{}'.format(team, prob) for team, prob in zip(power_rank_df['Team'], power_rank_df['PowerRank'])]

    # Define data for the graph
    data = [{
        'x': power_rank_df['TeamNickname'],
        'y': power_rank_df['PowerRank'],
        'yaxis': {'range': [0, 120]},
        'type': 'bar',
        'name': 'Power Rank',
        'text': hover_text,  # Set hover text
        'hoverinfo': 'text',  # Show only hover text
        'textposition': 'none'
    }]

    # Define layout for the graph
    layout = {
        'yaxis': {'title': 'Power Rank'},
        'showlegend': False,
        'dragmode': False,  # Disable zoom by click-and-drag
        'margin': {'t': 0, 'b': 30, 'l': 50, 'r': 15},
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
        'yaxis': {'range': [0, 100]},
        'type': 'bar',
        'name': 'Playoff Probability',
        'text': hover_text,  # Set hover text
        'hoverinfo': 'text',  # Show only hover text
        'textposition': 'none'
    }]

    # Define layout for the graph
    layout = {
        'yaxis': {'title': 'Probability (%)'},
        'showlegend': False,
        'dragmode': False,  # Disable zoom by click-and-drag
        'margin': {'t': 0, 'b': 30, 'l': 50, 'r': 15},
    }

    # Return the figure object with layout and configuration to disable interaction
    return {'data': data, 'layout': layout}
