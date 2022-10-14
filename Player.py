import socket
import time
import random


def SendMessage(requestmovemessage, socket, serverDetails):
    bytesToSend = str.encode(requestmovemessage)
    socket.sendto(bytesToSend, serverDetails)



class Player: 


    @classmethod
    def spawn(cls, serverDetails, playerName):
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        
        return Player(playerName, serverDetails, UDPClientSocket)
        

    def __init__(self, playername: str, serverDetails: tuple[str, int], socket):
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

        

    def join(self):
        join_command = "requestjoin:mydisplayname"
        join_bytes = str.encode(join_command)

        self.socket.sendto(join_bytes, self.serverDetails)
        update = self.socket.recvfrom(self.bufferSize)[0].decode('ascii')

        self.update(update)


    

    

    def move_to(self, x: int, y: int):
            requestmovemessage = f"moveto:{x},{y}"
            SendMessage(requestmovemessage)
            print(requestmovemessage)

    def fire(self):
        fireMessage = "fire:"
        SendMessage(fireMessage)
        print(fireMessage)

    def stop(self):
        stopMessage = "stop:"
        SendMessage(stopMessage)
        print(stopMessage)

    def move_direction(self, direction):
        directionMoveMessage = "movedirection:" + direction
        SendMessage(directionMoveMessage)
        print(directionMoveMessage)

    def face_direction(self):
        now = time.time()
        pass 
    


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

