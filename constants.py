#URLS
SCHEDULE_URL = 'https://www.400hitter.com/schedule.asp?SeID=364&m=506&show_team=0&show_ump=0&TmID=&CtID=0'
STANDINGS_URL = 'https://www.400hitter.com/standings.asp?SeID=364&CtID=0'
#Codes (Between 'SeID=' and '&m=50' in URLs):
#BMBL 2024: 364
#BMBL 2023: 353


#Calculation Constants
PYTHAG_EXPONENT = 0.287
MIN_STRENGTH = 0.001
MAX_STRENGTH = 0.999
HOME_FIELD_ADVANTAGE = 0.53

#Simulation Constants
NUM_SIMULATIONS = 1000
NUM_PLAYOFF_TEAMS = 6

#League Factors
END_OF_SEASON = False
PRESEASON = True
REGRESS_TO_MEAN = True
REGRESS_500_GAMES = 0.75
REGRESS_ESTIMATED = 0.8
REGRESS_PYTHAG = 0.2
REGRESS_LAST_YEAR = 1
LAST_YEAR_POWR_RANK = {'Merrimack Valley Marlins': 85.8,
    'Norfolk County Mariners': 61.9,
    'Middleboro Mocka Rays': 72.9,
    'South Shore Giants': 65,
    'Waltham Cutters': 62.1,
    'Granite State Rockies' : 35.8,
    'Boston Hogs': 42.5,
    'Greater Boston Bandits': 32,
    'Boston Phoenix': 45,
    'Weymouth Black Sox': 25.0,
    'Bay State Raiders': 30,
}