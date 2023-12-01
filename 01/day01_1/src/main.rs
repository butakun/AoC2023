fn main() {
    let filename = std::env::args().skip(1).next().unwrap();
    let lines = read(&filename);

    let mut sum: u32 = 0;
    for line in lines {
        let first: u32 = line.chars().find(|c| c.is_digit(10)).unwrap().to_digit(10).unwrap();
        let last: u32 = line.chars().rev().find(|c| c.is_digit(10)).unwrap().to_digit(10).unwrap();
        let value = first * 10 + last;
        sum += value;
        println!("{}, {}, {}, {}", line, first, last, value);
    }
    println!("sum = {sum}");
}

fn read(filename: &str) -> Vec<String> {
    std::fs::read_to_string(filename).unwrap()
        .trim()
        .split("\n")
        .map(|s| s.to_string())
        .collect()
}
