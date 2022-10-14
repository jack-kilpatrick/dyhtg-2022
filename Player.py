import socket
import time
import random


def SendMessage(requestmovemessage, socket, serverDetails):
    bytesToSend = str.encode(requestmovemessage)
    socket.sendto(bytesToSend, serverDetails)



class Player:

    # A list of all the actions the player can perform
    actions = ["join", "move_to", "fire", "stop", "move_direction", "face_direction"]

    # This is the time limit for socket operations such as recv
    socket_timeout = 30

    @classmethod
    def spawn(cls, serverDetails, playerName):
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        return Player(playerName, serverDetails, UDPClientSocket)

    def __init__(self, playername: str, serverDetails: tuple[str, int], socket):

        # This dictionary controls which actions are logged (displayed in the output)
        self.log_actions = {action: False for action in Player.actions}

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

        self.bufferSize          = 1024

        self.nearby_items = [] 
        self.seen_floors = []

        # Set the timeout for socket operations such as recvfrom
        socket.settimeout(Player.socket_timeout)

    def set_logging_for_action(self, action):
        if action in Player.actions:
            self.log_actions[action] = True
        else:
            print(f"{action} is not a valid action, so cannot be logged - ignoring...")

    def join(self):
        join_command = "requestjoin:mydisplayname"
        join_bytes = str.encode(join_command)

        self.socket.sendto(join_bytes, self.serverDetails)

        update = self.socket.recvfrom(self.bufferSize)[0].decode('ascii')


        self.update(update)


    

    

    def move_to(self, x: int, y: int):
            requestmovemessage = f"moveto:{x},{y}"
            SendMessage(requestmovemessage)
            if self.logging_actions["move_to"]:
                print(requestmovemessage)

    def fire(self):
        fireMessage = "fire:"
        SendMessage(fireMessage)
        if self.logging_actions["fire"]:
            print(fireMessage)

    def stop(self):
        stopMessage = "stop:"
        SendMessage(stopMessage)
        if self.logging_actions["stop"]:
            print(stopMessage)

    def move_direction(self, direction):
        directionMoveMessage = f"movedirection:{direction}"
        SendMessage(directionMoveMessage)
        if self.logging_actions["move_direction"]:
            print(directionMoveMessage)

    def face_direction(self, direction):
        directionFaceMessage = f"facedirection:{direction}"
        SendMessage(directionFaceMessage)
        if self.logging_actions["face_direction"]:
            print(directionFaceMessage)
    


    def update(self, update):
        components = update.split(':')
        dtype = components[0]
        data = components[1].split(',')

        if dtype == 'playerupdate':
            self.x = data[0]
            self.y = data[1]

            # what are data[2..4]

        elif dtype == 'nearbyitem':
            self.nearby_items.append(data)
            

        elif dtype == 'nearbyfloors':
            self.seen_floors.append(data)

        elif dtype == 'nearbywalls':
            pass

        else:
            print('ERR: unhandled update item', update)

