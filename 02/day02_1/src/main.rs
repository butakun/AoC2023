use std::collections::HashMap;

fn main() {
    let filename = std::env::args().skip(1).next().unwrap();
    let games = read(&filename);

    let mut possibles: _ = Vec::<u32>::new();
    for game_id in games.keys() {
        if is_possible(&games[game_id]) {
            possibles.push(*game_id);
        }
    }
    let sum: u32 = possibles.iter().sum();
    println!("{}", sum);
}

fn is_possible(sets: &Vec<HashMap<String, u32>>) -> bool {
    for a_set in sets {
        for (color, number) in a_set {
            if color == "red" && *number > 12 {
                return false;
            }
            if color == "green" && *number > 13 {
                return false;
            }
            if color == "blue" && *number > 14 {
                return false;
            }
        }
    }
    true
}

fn read(filename: &str) -> HashMap<u32, Vec<HashMap<String, u32>>> {
    let buf = std::fs::read_to_string(filename).unwrap();
    let lines: Vec<_> = buf
        .trim()
        .split("\n")
        .collect();

    lines.iter()
        .map(|line| {
            let mut tokens: Vec<&str> = line.split(":").collect();
            let game_id: u32 = tokens[0].split(" ").skip(1).next().unwrap().parse().unwrap();
            tokens = tokens[1].trim().split(";").map(|v| v.trim()).collect();
            let cube_sets = tokens
                .iter()
                .map(|buf_set| {
                    buf_set
                        .split(",")
                        .map(|v| {
                            let number_color: Vec<&str> = v.trim().split(" ").collect();
                            let number = number_color[0].parse::<u32>().unwrap();
                            let color = number_color[1].to_string();
                            (color, number)
                        })
                        .collect::<HashMap<String, u32>>()
                })
                .collect::<Vec<HashMap<String, u32>>>();
            (game_id, cube_sets)
        })
        .collect::<HashMap<u32, Vec<HashMap<String, u32>>>>()
}
