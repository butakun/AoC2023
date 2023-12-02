use std::collections::HashMap;

fn main() {
    let filename = std::env::args().skip(1).next().unwrap();
    let games = read(&filename);

    let mut sum: u32 = 0;
    for (game_id, game) in &games {
        let min_set = minimum_set(&game);
        let power = power(&min_set);
        println!("power = {power}");
        sum += power;
    }
    println!("sum = {sum}");
}

fn minimum_set(sets: &Vec<HashMap<String, u32>>) -> HashMap<String, u32> {
    let mut min: HashMap<String, u32> = HashMap::from(
        [ ("red".to_string(), 0), ("green".to_string(), 0), ("blue".to_string(), 0) ]
        );

    for a_set in sets {
        for (color, number) in a_set {
            if min[color] < *number {
                min.entry(String::from(color)).and_modify(|e| { *e = *number; });
            }
        }
    }
    min
}

fn power(set: &HashMap<String, u32>) -> u32 {
    set["red"] * set["green"] * set["blue"]
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
