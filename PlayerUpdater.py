
from Player import Player

if __name__ == '__main__':
    player1 = Player.spawn(("10.211.55.4", 11000),'lorne', verbose=True)
    # player1.socket.settimeout(0)
    players = [player1]

    while True:

        for p in players:
            
            # perform action then get update
            p.move_to(p.x+1, p.y+1)

            print(p.x, p.y)
            update = p.socket.recvfrom(p.bufferSize)[0].decode('ascii') 
            p.update(update, verbose=True)
            # Get the next 10 updates
            # for _ in range(10):
            #     update = p.socket.recvfrom(p.bufferSize)[0].decode('ascii') 
            #     p.update(update, verbose=True)

                