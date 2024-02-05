Dash WebApp that gets the live updating scores and schedule from Boston Men's Amateur Baseball League website and creates: Standings, Power Rankings, Single Game Outcome Predictor, and Playoff Probability


1. Standings:
Uses webcrawler to grab outcome of each game and create league standings updated to the minute.

2. Power Rankings:
Takes each team's performance thus far (Runs Scored, Runs Allowed, and Games Played) and applies Bill James' Pythagorean Win Probability formula to estimate each team's expected win percentage vs. a league average team. 
![Screen Shot 2024-02-04 at 11 18 03 PM](https://github.com/eweinhaus/baseball-power-rankings/assets/98419357/83e0f6ca-17b9-4962-b1d6-101ef8804e83)
Using a derivative of Tangotigers win probability forumla, factors in each team's home field advantage and strength of schedule into pythagorean win percentage in order to get adjusted expected winning percentage (Power Rank)
![Screen Shot 2024-02-04 at 11 35 22 PM](https://github.com/eweinhaus/baseball-power-rankings/assets/98419357/cb255c93-8331-43ae-9c97-dc4e568e36bf)

3. Single Game Outcome Predictor:
Applies Tangotiger's win probability formula to each team's power rank in order to estimate the percentage chance any home team beats any away team in a potential matchup.
![Screen Shot 2024-02-04 at 11 40 30 PM](https://github.com/eweinhaus/baseball-power-rankings/assets/98419357/78a790a6-b915-4c5e-807a-4524c92dfecd)
Utilizes Dash callbacks in order to allow user to input any potential matchup and estimate outcome in real time.

4. Playoff Probability:
Given current standings, power rankings, individual matchup win probability, and remaining schedule, app uses Pandas and Numpy to simulate the rest of the season 1000 times and graphs the probability that each team finishes top 5 in the standings in order to make the league playoffs.


