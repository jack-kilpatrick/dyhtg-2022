import socket
import time
import random


def SendMessage(requestmovemessage, socket, serverDetails):
    bytesToSend = str.encode(requestmovemessage)
    socket.sendto(bytesToSend, serverDetails)



class Player: 


    @classmethod
    def spawn(cls, serverDetails, playerName, verbose=False):
        print('spawning', playerName)
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        
        return Player(playerName, serverDetails, UDPClientSocket, verbose=verbose)
        

    def __init__(self, playername: str, serverDetails: tuple[str, int], socket, verbose=False):
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
        self.seen_walls = [] 
        self.verbose = verbose


        self.join()

        

    def join(self):
        if self.verbose:
            print('joining')
        join_command = "requestjoin:" + self.playername
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
        directionMoveMessage = f"movedirection:{direction}"
        SendMessage(directionMoveMessage)
        print(directionMoveMessage)

    def face_direction(self, direction):
        directionFaceMessage = f"facedirection:{direction}"
        SendMessage(directionFaceMessage)
        print(directionFaceMessage)
    


    def update(self, update):
        if self.verbose:
            print('updating')
        components = update.split(':')
        dtype = components[0]
        data = components[1].split(',')

        if self.verbose:
            print(dtype, data)

        if dtype == 'playerupdate':
            self.x = int(data[0])
            self.y = int(data[1])

            # what are data[2..4]

        elif dtype == 'nearbyitem':
            self.nearby_items.append(data)
            
        elif dtype == 'nearbyfloors':
            self.seen_floors.append(data)

        elif dtype == 'nearbywalls':
            self.seen_walls.append(data)

        elif dtype == 'playerjoined':
            self.x = int(data[2])
            self.y = int(data[3])
            self.type = data[0]

            if self.verbose:
                print('Player', self.playername, 'joined as', self.type, f'at position {self.x}, {self.y}'  )
            

        else:
            print('ERR: unhandled update item', update)

