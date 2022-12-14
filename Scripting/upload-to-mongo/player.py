
class Player:
    def __init__(self, name, position, team, birthday, gameday, injurystatus):
        self.Player = name
        self.Position = position
        self.Team = team
        self.Birthday = birthday
        self.GameDay = gameday
        self.InjuryStatus = injurystatus

    def __eq__(self, other):
        equivalent = 
            self.Player == other.Player and
            self.Position == other.Position and
            self.Team == other.Team and
            self.Birthday == other.Birthday and
            self.GameDay == other.GameDay and
            self.InjuryStatus == other.InjuryStatus

    def __hash__(self):
        return hash(self.Player)
