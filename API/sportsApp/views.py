""""
End points
"""

from django.http import JsonResponse
from .models import Player
from .serializers import PlayerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def player_list(request, format=None):

    if request.method == 'GET':
        # get player list
        players = Player.objects.all()
        # serialize them
        serializer = PlayerSerializer(players, many=True)
        # return JSON
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = PlayerSerializer(data=request.data)
        # check for valid data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def player_detail_plus(request, id, format=None):

#     try:
#         player = Player.objects.get(pk=id) # pk is the primary key
#     except Player.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = PlayerSerializer(player)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = PlayerSerializer(player, data=request.data)
#         # check for valid data
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         player.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def player_detail(request, format=None):
    try:
        player = Player.objects.get(pk=id) # pk is the primary key
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(player)
        return Response(serializer.data)