
if __name__ == '__main__':
    import random
    from FloorTile import FloorTile
    from Wall import Wall
    from time import sleep

    from Player import Player

    player1 = Player.spawn(("10.211.55.4", 11000), 'lorne')
    print(player1.x, player1.y)
    player1.x += 4
    player1.y += 4


    def update():
        for _ in range(100):
            update = player1.socket.recvfrom(player1.bufferSize)[0].decode('ascii')
            player1.update(update)


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
        sleep(1)

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

            if i % 2 == 0:
                update()
            sleep(1)


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
        sleep(1)

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

            if i % 2 == 0:
                update()
            sleep(1)


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
        sleep(1)

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

            if i % 2 == 0:
                update()
            sleep(1)


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

        sleep(1)
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

            if i % 2 == 0:
                update()
            sleep(1)


    if player1.playertype == 'warrior':
        update()
        east()

    elif player1.playertype == 'valkyrie':
        update()
        south()

    elif player1.playertype == 'elf':
        update()
        west()

    elif player1.playertype == 'wizard':
        update()
        north()
