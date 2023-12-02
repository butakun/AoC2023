def read(filename):
    games = {}
    for line in open(filename):
        game_id = int(line.split(":")[0].split()[1])
        sets = line.split(":")[1].split(";")
        game = []
        for sett in sets:
            cubes = sett.split(",")
            a_set = {}
            for cube in cubes:
                n, color = cube.split()
                color = color.strip(",")
                a_set[color] = int(n)
            game.append(a_set)
        games[game_id] = game
    return games


def main(filename):
    total = {"red": 12, "green": 13, "blue": 14}
    games = read(filename)

    possibles = []
    for game_id, game in games.items():
        impossible = False
        print(game_id, game)
        for a_set in game:
            for color, number in a_set.items():
                if total[color] < number:
                    print(f"{game_id} impossible becaus {number} {color}")
                    impossible = True
                    break
            if impossible:
                break
        if not impossible:
            possibles.append(game_id)

    print(sum(possibles))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
