struct Symbol {
    c: char,
    pos: (i32, i32),
}

struct Number {
    value: u32,
    len: i32,
    pos: (i32, i32),
}

impl Number {
    fn new(value: &str, pos: (i32, i32)) -> Self {
        Number {
            value: value.clone().parse::<u32>().unwrap(),
            len: value.len() as i32,
            pos: pos,
        }
    }

    fn is_adjacent_to(&self, pos: (i32, i32)) -> bool {
        let i_min = self.pos.0 - 1;
        let i_max = self.pos.0 + 1;
        let j_min = self.pos.1 - 1;
        let j_max = self.pos.1 + self.len;
        (i_min <= pos.0) && (pos.0 <= i_max) && (j_min <= pos.1) && (pos.1 <= j_max)
    }
}

fn main() {
    let filename = std::env::args().skip(1).next().unwrap();
    let (symbols, numbers) = read(&filename);

    let mut sum: u32 = 0;
    for symbol in &symbols {
        if symbol.c != '*' {
            continue;
        }

        let mut count: u32 = 0;
        let mut cogs = Vec::<u32>::new();
        for (i, number) in numbers.iter().enumerate() {
            if number.is_adjacent_to(symbol.pos) {
                if count == 2 {
                    break;
                }
                println!("{} is adjacent to {} in ({}, {})", number.value, symbol.c, symbol.pos.0, symbol.pos.1);
                count += 1;
                cogs.push(number.value);
            }
        }
        if count == 2 {
            let ratio = cogs[0] * cogs[1];
            println!("{} x {} = {}", cogs[0], cogs[1], ratio);
            sum += ratio;
        }
    }
    println!("sum = {}", sum);
}

fn read(filename: &str) -> (Vec<Symbol>, Vec<Number>) {
    let lines: Vec<String> = std::fs::read_to_string(filename).unwrap().split("\n").map(|s| s.to_string()).collect();

    let mut symbols = Vec::<Symbol>::new();
    let mut numbers = Vec::<Number>::new();

    for (i, line) in lines.iter().enumerate() {
        let mut number = String::new();
        for (j, c) in line.chars().enumerate() {
            if c.is_digit(10) {
                number.push(c);
            } else {
                if number.len() > 0 {
                    let jc = j - number.len();
                    let num = Number::new(&number, (i as i32, jc as i32));
                    numbers.push(num);
                    number.clear();
                }
                if c != '.' {
                    let sym = Symbol {c: c, pos: (i as i32, j as i32)};
                    symbols.push(sym)
                }
            }
        }
        if number.len() > 0 {
            let jc = line.len() - number.len();
            let num = Number::new(&number, (i as i32, jc as i32));
            numbers.push(num);
            number.clear();
        }
    }
    (symbols, numbers)
}
