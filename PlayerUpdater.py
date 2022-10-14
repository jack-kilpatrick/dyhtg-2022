
from Player import Player

if __name__ == '__main__':
    player1 = Player.spawn(("10.211.55.4", 11000),'lorne' )
    players = [player1]

    while True:

        for p in players:

            # Get the next 10 updates
            for _ in range(10):
                update = p.socket.recvfrom(p.bufferSize)[0].decode('ascii') 
                p.update(update)

                