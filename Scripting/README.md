# Plan
Start with NFL birthdays on gameday

## Research checkpoints
- Get NFL player's birthdays [ x ] -> https://nflbirthdays.com/
- Get every team's schedule [  ] - espn hidden API -> https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b &&https://www.reddit.com/r/NFLstatheads/comments/p4n7dm/can_i_pull_the_entire_seasons_schedule_down_from/
    - http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype=2&week=${week}
- Find the players that have birthdays that match week 1 through 18 -> 


### TODO
- write scraped schedule to csv
- compare each player's birthday, add to new csv file when they play on their birthday
    - Add in data like: home or away, conference play, position
    - Check if birthday is within the season
        - if not move ot next player
    - 

LATER:
    - scrape player data to check if the player is healthy or not