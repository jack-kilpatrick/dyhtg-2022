import sys
from Player import Player

if __name__ == '__main__':
    player1 = Player.spawn(("10.211.55.4", 11000),'lorne')
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

        for p in players:

            if p.joined_server:
            
                # perform action then get update
                p.move_to(p.x+1, p.y+1)

                print(p.x, p.y)
                try:
                    update = p.socket.recvfrom(p.bufferSize)[0].decode('ascii')
                except TimeoutError:
                    print("Connection to server timed out - exiting...")
                    break
                p.update(update, verbose=True)
                # Get the next 10 updates
                # for _ in range(10):
                #     update = p.socket.recvfrom(p.bufferSize)[0].decode('ascii')
                #     p.update(update, verbose=True)

            else:
                print(f"Failed to join server with player: {p.playername}")
