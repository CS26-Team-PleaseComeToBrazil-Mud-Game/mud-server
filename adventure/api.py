from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config(
# 'PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    # set currentWorld
    player.currentWorld = World.objects.all().last().uuid
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    player.save()
    return JsonResponse({'uuid': uuid, 'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players}, safe=True)

# create_world endpoint


"""
{
    width: 2,
    height: 2,
    rooms: {
        r0c0: {
            title: "apple",
            column: 0,
            row: 0,
            n_to: null,
            s_to: {row: 1, col: 0},
            e_to: null,
            w_to: null,
            tile_num: 3,
        },
    }
}
"""
@csrf_exempt
@api_view(["GET"])
def world(request):
    """Return the map
    """
    user = request.user
    player = user.player
    # get world width and height
    world = World.objects.get(uuid=player.currentWorld)

    # add to data
    data = {'world': world.uuid, 'width': world.width, 'height': world.height}

    # get rooms
    rooms = Room.objects.filter(world=player.currentWorld)
    data['room_count'] = rooms.count()
    for room in rooms:
        # add rooms to return object
        data[f'r{room.row}c{room.col}'] = {'title': room.title, 'description': room.description,
                                           'n': room.n_to, 's': room.s_to, 'e': room.e_to, 'w': room.w_to, 'tile_num': room.tile_num}

    return JsonResponse({'data': data})


@csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = request.data
    direction = data['direction']
    room = player.room()
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom = nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {
        #                    'message': f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {
        #                    'message': f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name': player.user.username, 'title': nextRoom.title, 'description': nextRoom.description, 'players': players, 'error_msg': ""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'error_msg': "You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error': "Not yet implemented"}, safe=True, status=500)
