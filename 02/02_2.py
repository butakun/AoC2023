def read(filename):
    games = {}
    for line in open(filename):
        game_id = int(line.split(":")[0].split()[1])
        sets = line.split(":")[1].split(";")
        game = []
        for sett in sets:
            tokens = sett.split()
            a_set = {}
            for i in range(int(len(tokens) / 2)):
                n = int(tokens[2 * i])
                color = tokens[2 * i + 1].strip(",")
                a_set[color] = n
            game.append(a_set)
        games[game_id] = game
    return games


def main(filename):
    games = read(filename)

    powers = []
    for game_id, game in games.items():
        print(game_id, game)
        minimum = {"red": 0, "green": 0, "blue": 0}
        for a_set in game:
            for color, number in a_set.items():
                minimum[color] = max(number, minimum[color])
        print(f"  min set is {minimum}")
        power = minimum["red"] * minimum["green"] * minimum["blue"]
        print(f"  power = {power}")
        powers.append(power)

    print(sum(powers))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
