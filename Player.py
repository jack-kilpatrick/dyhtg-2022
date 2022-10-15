import socket
import time
import random
import sys
from FloorTile import FloorTile
from Item import Item
from math import sqrt


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
        self.y = None
        self.x = None
        self.logging_actions = {action: False for action in self.actions}

        self.moveInterval = 10
        self.timeSinceMove = time.time()

        self.fireInterval = 5
        self.timeSinceFire = time.time()

        self.stopInterval = 30
        self.timeSinceStop = time.time()

        self.directionMoveInterval = 15
        self.timeSinceDirectionMove = time.time()

        self.directionFaceInterval = 9
        self.timeSinceDirectionFace = time.time()

        self.playername = playername
        self.serverDetails = serverDetails

        self.socket = socket

        self.bufferSize = 1024

        self.nearby_items = set()
        self.seen_floors = set()

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
        join_command = "requestjoin:" + self.playername
        join_bytes = str.encode(join_command)

        self.socket.sendto(join_bytes, self.serverDetails)
        update = self.socket.recvfrom(self.bufferSize)[0].decode('ascii')

        self.update(update)

    def SendMessage(self, requestmovemessage):
        bytesToSend = str.encode(requestmovemessage)
        self.socket.sendto(bytesToSend, self.serverDetails)

    def move_to(self, x: int, y: int):
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

        print(dtype, data)

        if dtype == 'playerupdate':
            # self.x = int(data[0])
            # self.y = int(data[1])

            # what are data[2..4]
            pass

        elif dtype == 'nearbyitem':
            # self.nearby_items.append(data)

            if len(data):
                n_groups = (len(data) - 1) // 3
                for i in range(n_groups):
                    itemtype, x, y = data[i * 3:(i + 1) * 3]
                    self.nearby_items.add(Item(itemtype, x, y))

        elif dtype == 'nearbyfloors':
            # Each floor tile comes in the format x1,y1,x2,y2,...
            if len(data):
                n_groups = (len(data) - 1) // 2

                for i in range(n_groups):
                    x, y = data[i * 2:(i + 1) * 2]
                    ft = FloorTile(int(x), int(y), False)

                    self.seen_floors.add(ft)

        elif dtype == 'playerjoined':
            self.x = int(data[2])
            self.y = int(data[3])


        elif dtype == 'nearbywalls':
            pass

        else:
            print('ERR: unhandled update item', update)

    def nearest_floors(self, k):

        def distance(floor: FloorTile):
            return sqrt(
                (self.x - floor.x) ** 2 + (self.y - floor.y) ** 2
            )

        k_nearest_floors = sorted(self.seen_floors, key=distance)[:k]

        return k_nearest_floors
