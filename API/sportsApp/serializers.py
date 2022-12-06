from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        # model data
        model = Player
        fields = ['id', 'Sport', 'PlayerName', 'Position', 'Team', 'Birthday', 'GameDay', 'InjuryStatus']
