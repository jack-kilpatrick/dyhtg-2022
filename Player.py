import socket
import time
import random


def SendMessage(requestmovemessage, socket, serverDetails):
    bytesToSend = str.encode(requestmovemessage)
    socket.sendto(bytesToSend, serverDetails)



class Player: 


    @staticmethod
    def spawn(cls, serverDetails, playerName):
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        
        return cls(playerName, serverDetails, UDPClientSocket)
        

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


    
    def spawn(self):
        
    

    def move_to(self, x: int, y: int):
        now = time.time()
        pass

    def fire(self):
        now = time.time()
        pass

    def stop(self):
        now = time.time()
        pass 

    def move_direction(self):
        now = time.time()
        pass

    def face_direction(self):
        now = time.time()
        pass 
    
