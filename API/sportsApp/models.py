from django.db import models

class Player(models.Model):
    Sport = models.CharField(max_length=50)
    PlayerName = models.CharField(max_length=50)
    Position = models.CharField(max_length=50)
    Team = models.CharField(max_length=50)
    Birthday = models.CharField(max_length=50)
    GameDay = models.CharField(max_length=50)
    InjuryStatus = models.CharField(max_length=50)
    def __str__(self):
        return self.PlayerName