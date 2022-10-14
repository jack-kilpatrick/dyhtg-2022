import sys
from Player import Player
import time

if __name__ == '__main__':
    
    player1 = Player.spawn(("10.211.55.1", 11000),'lorne')
    # player1.socket.settimeout(0)
    players = [player1]

    # The actions we want to display as script output for each player
    actions_to_log = []

    args = sys.argv
    for arg in args:
        if arg[:4] == "log:":
            if arg[4:] == "all":
                actions_to_log = Player.actions
            else:
                actions_to_log = arg[4:].split(",")

    for player in players:
        for action in actions_to_log:
            player.set_logging_for_action(action)

    while True:
        time.sleep(1)

        for p in players:
            
            # perform action then get update
            print(p.x, p.y)
            p.move_to(p.x+1, p.y)

            
            update = p.socket.recvfrom(p.bufferSize)[0].decode('ascii') 
            p.update(update)
            # Get the next 10 updates
            

        