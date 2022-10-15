import socket
import time
import random
import sys
from FloorTile import FloorTile
from Item import Item
from math import sqrt
from Wall import Wall
from Exit import Exit


class Player:

    # A list of all the actions the player can perform
    actions = ["join", "move_to", "fire", "stop", "move_direction", "face_direction"]

    @classmethod
    def spawn(cls, serverDetails, playerName):
        try:
            UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        except socket.error as e:

            print("Error creating socket: ", e)
            sys.exit(1)
        
        return Player(playerName, serverDetails, UDPClientSocket)

    def __init__(self, playername: str, serverDetails: tuple[str, int], socket):

        # This dictionary controls which actions are logged (displayed in the output)

        self.logging_actions = {action: False for action in self.actions}

        self.playername = playername
        self.y = None
        self.x = None
        self.logging_actions = {action: False for action in self.actions}
        self.health = 0
        self.ammo = 0

        self.seen_items = set()
        self.seen_floors = set()
        self.seen_walls = set()

        self.predecessors = {}

        self.serverDetails = serverDetails
        self.socket = socket
        self.bufferSize = 1024

        self.exit = None

        self.join()

    def get_player_actions(self, action):
        return self.actions

    def set_logging_for_action(self, action):
        if action in self.actions:
            self.logging_actions[action] = True

    def set_logging_for_action(self, action):
        if action in self.actions:
            self.log_actions[action] = True
        else:
            print(f"{action} is not a valid action, so cannot be logged - ignoring...")

    def join(self):
        join_command = "requestjoin:mydisplayname"
        join_bytes = str.encode(join_command)

        self.socket.sendto(join_bytes, self.serverDetails)

        try:
            update = self.socket.recvfrom(self.bufferSize)[0].decode('ascii')
        except TimeoutError:
            self.joined_server = False
            print(f"Failed to join server with player: {self.playername}")
        else:
            self.joined_server = True
            self.update(update)

    def SendMessage(self, requestmovemessage):
        bytesToSend = str.encode(requestmovemessage)
        self.socket.sendto(bytesToSend, self.serverDetails)

    def move_to(self, x: int, y: int):

        self.predecessors[f'{x},{y}'] = f'{self.x},{self.y}'
        self.x = x
        self.y = y

        requestmovemessage = f"moveto:{x},{y}"
        self.SendMessage(requestmovemessage)
        if self.logging_actions["move_to"]:
            print(requestmovemessage)

    def fire(self):
        fireMessage = "fire:"
        self.SendMessage(fireMessage)
        if self.logging_actions["fire"]:
            print(fireMessage)

    def stop(self):
        stopMessage = "stop:"
        self.SendMessage(stopMessage)
        if self.logging_actions["stop"]:
            print(stopMessage)

    def move_direction(self, direction):
        directionMoveMessage = f"movedirection:{direction}"
        self.SendMessage(directionMoveMessage)
        if self.logging_actions["move_direction"]:
            print(directionMoveMessage)

    def face_direction(self, direction):
        directionFaceMessage = f"facedirection:{direction}"
        self.SendMessage(directionFaceMessage)
        if self.logging_actions["face_direction"]:
            print(directionFaceMessage)

    def update(self, update):
        components = update.split(':')
        dtype = components[0]
        data = components[1].split(',')

        # print(dtype, data)

        if dtype == 'playerupdate':
            # self.x = int(data[0])
            # self.y = int(data[1])
            self.health = int(data[2])
            self.ammo = int(data[3])

            # what are data[2..4]

        elif dtype == 'nearbyitem':
            # self.nearby_items.append(data)

            if len(data):
                n_groups = (len(data) - 1) // 3
                for i in range(n_groups):
                    itemtype, x, y = data[i * 3:(i + 1) * 3]
                    self.seen_items.add(Item(itemtype, x, y))

        elif dtype == 'nearbyfloors':
            # Each floor tile comes in the format x1,y1,x2,y2,...
            if len(data):
                n_groups = (len(data) - 1) // 2

                for i in range(n_groups):
                    x, y = data[i * 2:(i + 1) * 2]
                    ft = FloorTile(int(x), int(y), False)

                    self.seen_floors.add(ft)

        elif dtype == 'playerjoined':
            print('joined with data', data)
            self.x = int(data[2])
            self.y = int(data[3])

        elif dtype == 'nearbywalls':
            if len(data):
                n_groups = (len(data) - 1) // 2

                for i in range(n_groups):
                    x, y = data[i * 2:(i + 1) * 2]
                    ft = Wall(int(x), int(y))

                    self.seen_walls.add(ft)

        elif dtype == 'exit':
            if len(data):
                self.exit = Exit(int(data[0]), int(data[1]))

        else:
            print('ERR: unhandled update item', update)

    def nearest_floors(self, k):

        def distance(floor: FloorTile):
            return sqrt(
                (self.x - floor.x) ** 2 + (self.y - floor.y) ** 2
            )

        k_nearest_floors = sorted(self.seen_floors, key=distance)[:k]

        return k_nearest_floors

    def nearest_walls(self, k):

        def distance(wall: Wall):
            return sqrt(
                (self.x - wall.x) ** 2 + (self.y - wall.y) ** 2
            )

        k_nearest_walls = sorted(self.seen_walls, key=distance)[:k]

        return k_nearest_walls

    def nearest_items(self, k):

        def distance(item: Item):
            return sqrt(
                (self.x - item.x) ** 2 + (self.y - item.y) ** 2
            )

        k_nearest_items = sorted(self.seen_items, key=distance)[:k]

        return k_nearest_items
