import sys
from Player import Player
from FloorTile import FloorTile
from time import sleep
import socket
import random
from Wall import Wall

if __name__ == '__main__':
    player1 = Player.spawn(("localhost", 11000),'jack')
    players = [player1]
    joined_players = [player for player in players if player.joined_server]

    # The actions we want to display as script output for each player
    actions_to_log = []

    args = sys.argv
    for arg in args:
        if arg[:4] == "log:":
            if arg[4:] == "all":
                actions_to_log = Player.actions
            else:
                actions_to_log = arg[4:].split(",")

    for player in joined_players:
        for action in actions_to_log:
            player.set_logging_for_action(action)

    def update_players():
        for player in joined_players:
            for _ in range(10):
                update_message = player.socket.recvfrom(player1.bufferSize)[0].decode('ascii')
                print(update_message)
                player.update(update_message)

    def get_items():
        if 'treasure' in player1.seen_items_dict:
            player1.get_item('treasure')
        if 'redkey' in player1.seen_items_dict:
            player1.get_item('redkey')
        if 'redkey' in player1.inventory_dict and 'exit' in player1.seen_items_dict:
            player1.get_item('exit')

    # Move up to the outer wall and start traversing
    while (player1.x, player1.y-8) not in player1.seen_walls_dict:
        player1.move_direction("n")
        update_players()
    player1.stop()

    player1.face_direction("w")

    while True:

        while player1.get_tile_on_right() in player1.seen_walls_dict and player1.get_tile_in_front() not in player1.seen_walls_dict:
            x, y = player1.get_tile_in_front()
            player1.move_to(x, y)
            update_players()
            get_items()

        if player1.get_tile_on_right() not in player1.seen_walls_dict:
            player1.face_right()
            x, y = player1.get_tile_in_front()
            player1.move_to(x, y)
            update_players()
            get_items()

        elif player1.get_tile_in_front() in player1.seen_walls_dict:
            player1.face_left()