#URLS
SEASON_ID = 377
SCHEDULE_URL = f'https://www.400hitter.com/schedule.asp?SeID={SEASON_ID}&m=506&show_team=0&show_ump=0&TmID=&CtID=0'
STANDINGS_URL = f'https://www.400hitter.com/standings.asp?SeID={SEASON_ID}&CtID=0'
LAST_UPDATE = "****"
#Season IDs:
#BMBL 2025: 377
#BMBL 2024: 364
#BMBL 2023: 353



#Calculation Constants
PYTHAG_EXPONENT = 0.287
MIN_STRENGTH = 0.001
MAX_STRENGTH = 0.999
HOME_FIELD_ADVANTAGE = 0.53

#Simulation Constants
NUM_SIMULATIONS = 1250
NUM_PLAYOFF_TEAMS = 6

#League Factors
END_OF_SEASON = False
PRESEASON = False
REGRESS_TO_MEAN = True
REGRESS_500_GAMES = 0.25
REGRESS_ESTIMATED = 1.2
REGRESS_PYTHAG = 0.2
REGRESS_LAST_YEAR = 0.1
LAST_YEAR_POWR_RANK = {'Merrimack Valley Marlins': 71.4,
    'Norfolk County Mariners': 66.8,
    'Middleboro Mocka Rays': 82.3,
    'South Shore Giants': 42.0,
    'Waltham Cutters': 43.4,
    'Granite State Rockies' : 35.0,
    'Boston Hogs': 59.2,
    'Greater Boston Bandits': 43.3,
    'Boston Phoenix': 52.2,
    'Weymouth Black Sox': 32.8,
    'Bay State Raiders': 26.1,
    #'Malden Marlins': 80,
}


# TEAM_COLORS = {
#     'Merrimack Valley Marlins': 'darkblue',
#     'Norfolk County Mariners': '#E3DEB1',
#     'Middleboro Mocka Rays': '#F9D655',
#     'South Shore Giants': '#DA4E30',
#     'Waltham Cutters': '#0E2A53',
#     'Granite State Rockies' : '#78388D',
#     'Boston Hogs': '#E93732',
#     'Greater Boston Bandits': '#EC3940',
#     'Boston Phoenix': '#EBA53E',
#     'Weymouth Black Sox': '#090909',
#     'Bay State Raiders': '#2C5E1B'
# }

TEAM_COLORS = {
    'Merrimack Valley Marlins': ['#2A7FC3', '#2A7FC3'],
    'Norfolk County Mariners': ['#E3DEB1', '#041351'],
    'Middleboro Mocka Rays': ['#F9D655', 'darkblue'],
    'South Shore Giants': ['#DA4E30', '#DA4E30'],
    'Waltham Cutters': ['#0E2A53', '#0E2A53'],
    'Granite State Rockies' : ['#78388D', '#78388D'],
    'Boston Hogs': ['#E93732', '#E93732'],
    'Greater Boston Bandits': ['black', '#EC3940'],
    'Boston Phoenix': ['#EBA53E', '#E93F32'],
    'Weymouth Black Sox': ['#090909', '#090909'],
    'Bay State Raiders': ['#2C5E1B', '#2C5E1B'],
    'Malden Marlins': ['#FFFFFF', '#000000']
    
}
