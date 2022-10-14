import socket
import time
import random
import sys




class Player: 


    @classmethod
    def spawn(cls, serverDetails, playerName):
        try:
            UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        except socket.error as e:

            print("Error creating socket: ", e)
            sys.exit(1)
        
        return Player(playerName, serverDetails, UDPClientSocket)
        

    def __init__(self, playername: str, serverDetails: tuple[str, int], socket):

        # A list of all the actions the player can perform
        self.actions = ["join", "move_to", "fire", "stop", "move_direction", "face_direction"]

        # This dictionary controls which actions are logged (displayed in the output)
        self.logging_actions = {action:False for action in self.actions}

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

        self.nearby_items = [] 
        self.seen_floors = []


        self.join() 

    def get_player_actions(self, action):
        return self.actions

    def set_logging_for_action(self,action):
        if action in self.actions:
            self.logging_actions[action] = True
        else:
            print(f"{action} is not a valid action, so cannot be logged - ignoring...")

    def join(self):
        join_command = "requestjoin:mydisplayname"
        join_bytes = str.encode(join_command)

        self.socket.sendto(join_bytes, self.serverDetails)
        update = self.socket.recvfrom(self.bufferSize)[0].decode('ascii')

        self.update(update)


    def SendMessage(self, requestmovemessage ):
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
            self.x = int(data[0])
            self.y = int(data[1])

            # what are data[2..4]

        elif dtype == 'nearbyitem':
            # self.nearby_items.append(data)

            if len(data):
                n_groups = (len(data)-1) // 3
                for i in range(n_groups):

                    self.nearby_items.append(data[i*3:(i+1)*3])
            

        elif dtype == 'nearbyfloors':
            self.seen_floors.append(data)

        elif dtype == 'playerjoined':
            self.x = int(data[2] ) 
            self.y = int(data[3]) 
        

        elif dtype == 'nearbywalls':
            pass

        else:
            print('ERR: unhandled update item', update)

