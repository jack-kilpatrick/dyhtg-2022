import sys
from Player import Player
from FloorTile import FloorTile
from time import sleep
import socket
import random
from Wall import Wall

if __name__ == '__main__':
    player1 = Player.spawn(("10.211.55.4", 11000),'lorne')
    # player1.socket.settimeout(0)
    players = [player1]

    joined_players = [player for player in players if player.joined_server]

    # The actions we want to display as script output for each player
    actions_to_log = []

    args = sys.argv
    for arg in args:
        if arg[:4] == "log:":
            if arg[4:] == "all":
                actions_to_log = Player.actions
            else:
                actions_to_log = arg[4:].split(",")

    for player in joined_players:
        for action in actions_to_log:
            player.set_logging_for_action(action)

    # def update():
    #     for _ in range(50):
    #         u = player1.socket.recvfrom(player1.bufferSize)[0].decode('ascii')
    #         player1.update(u)

    def update():
        player1.stop()
        player1.socket.close()
        player1.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        player1.join()
        #     player1.x += 4
        #     player1.y += 4

        for _ in range(64):
            update = player1.socket.recvfrom(player1.bufferSize)[0].decode('ascii')
            player1.update(update)


    sleeptime = 0.75
    updatefreq = 3

    # lastpos = player1.x,player1.y
    i = 0
    while True:

        if i % updatefreq == 0:
            update()

        left_square = player1.x - 8, player1.y
        sq = FloorTile(*left_square, False)

        print('wanting to move to square', sq, 'from', player1.x, player1.y)
        if sq in player1.seen_walls:
            print('reached the wall at', sq)
            break

        player1.move_to(sq.x, sq.y)

        i += 1
        sleep(sleeptime)

    n = player1.x, player1.y - 8
    s = player1.x, player1.y + 8
    e = player1.x + 8, player1.y
    w = player1.x - 8, player1.y

    ntile, stile, etile, wtile = [FloorTile(*i, False) for i in [n, s, e, w]]

    update()


    def north():
        #     update()

        print('Heading north')

        n = player1.x, player1.y - 8
        ntile = FloorTile(*n, False)

        if ntile in player1.seen_walls:
            east()
            print("should head east")
            return

        player1.move_to(ntile.x, ntile.y)
        sleep(sleeptime)

        i = 0

        while True:

            n = player1.x, player1.y - 8
            ntile = FloorTile(*n, False)

            s = player1.x, player1.y + 8
            e = player1.x + 8, player1.y
            w = player1.x - 8, player1.y

            stile, etile, wtile = [FloorTile(*i, False) for i in [s, e, w]]

            if wtile not in player1.seen_walls:
                west()
                print("sould head west")
                return

            if ntile in player1.seen_walls:
                east()
                print("should head east")
                return

            player1.move_to(ntile.x, ntile.y)

            i += 1

            if i % updatefreq == 0:
                update()
            sleep(sleeptime)


    def east():
        #     update()
        print('Heading east')

        e = player1.x + 8, player1.y
        etile = FloorTile(*e, False)

        if etile in player1.seen_walls:
            print('should head south')
            south()
            return

        player1.move_to(etile.x, etile.y)
        sleep(sleeptime)

        i = 0

        while True:

            e = player1.x + 8, player1.y
            etile = FloorTile(*e, False)

            n = player1.x, player1.y - 8
            s = player1.x, player1.y + 8

            w = player1.x - 8, player1.y

            ntile, stile, wtile = [FloorTile(*i, False) for i in [n, s, w]]

            if ntile not in player1.seen_walls:
                print('should head north')
                north()

                return

            if etile in player1.seen_walls:
                print('should head south')
                south()
                return

            player1.move_to(etile.x, etile.y)
            i += 1

            if i % updatefreq == 0:
                update()
            sleep(sleeptime)


    def south():
        print('Heading south')

        s = player1.x, player1.y + 8
        stile = FloorTile(*s, False)

        if stile in player1.seen_walls:
            #
            print('should head west')
            west()
            return

        player1.move_to(stile.x, stile.y)
        sleep(sleeptime)

        i = 0
        while True:

            s = player1.x, player1.y + 8
            stile = FloorTile(*s, False)

            n = player1.x, player1.y - 8

            e = player1.x + 8, player1.y
            w = player1.x - 8, player1.y

            ntile, etile, wtile = [FloorTile(*i, False) for i in [n, e, w]]

            if etile not in player1.seen_walls:
                print('should head east')
                east()
                return

            if stile in player1.seen_walls:
                #
                print('should head west')
                west()
                return

            player1.move_to(stile.x, stile.y)
            i += 1

            if i % updatefreq == 0:
                update()
            sleep(sleeptime)


    def west():
        #     update()
        print('Heading west')

        w = player1.x - 8, player1.y
        wtile = FloorTile(*w, False)

        if wtile in player1.seen_walls:
            print('Should head north')
            north()
            return

        player1.move_to(wtile.x, wtile.y)

        sleep(sleeptime)
        i = 0

        while True:

            w = player1.x - 8, player1.y
            wtile = FloorTile(*w, False)

            n = player1.x, player1.y - 8
            e = player1.x + 8, player1.y
            s = player1.x, player1.y + 8

            ntile, stile, etile = [FloorTile(*i, False) for i in [n, s, e]]

            if stile not in player1.seen_walls:
                print('should head south')
                south()
                return

            if wtile in player1.seen_walls:
                print('Should head north')
                north()
                return

            player1.move_to(wtile.x, wtile.y)

            i += 1

            if i % updatefreq == 0:
                update()
            sleep(sleeptime)


    north()

