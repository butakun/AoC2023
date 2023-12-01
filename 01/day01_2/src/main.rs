fn main() {
    let filename = std::env::args().skip(1).next().unwrap();
    let lines = read(&filename);

    let mut sum: u32 = 0;
    for line in lines {
        let (first, last) = find_digits(&line);
        let value = first * 10 + last;
        println!("{line}: {first}, {last}, {value}");
        sum += value;
    }
    println!("sum = {sum}");
}

fn find_digits(line: &str) -> (u32, u32) {
    let words = vec!["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"];

    let mut index_first: usize = line.len();
    let mut index_last: usize = 0;
    let mut digit_first: Option<u32> = None;
    let mut digit_last: Option<u32> = None;

    for (i, c) in line.chars().enumerate() {
        if c.is_digit(10) {
            if i < index_first {
                index_first = i;
                digit_first = c.to_digit(10);
            }
            if i >= index_last {
                index_last = i;
                digit_last = c.to_digit(10);
            }
        }
    }

    for (d, word) in words.iter().enumerate() {
        let digit = d as u32 + 1;
        let indices: Vec<_> = line.match_indices(word).map(|m| m.0).collect();
        if indices.len() > 0 {
            let imin = indices.iter().min().unwrap();
            let imax = indices.iter().max().unwrap();
            if imin < &index_first {
                index_first = *imin;
                digit_first = Some(digit);
            }
            if imax >= &index_last {
                index_last = *imax;
                digit_last = Some(digit);
            }
        }
    }

    (digit_first.unwrap(), digit_last.unwrap())
}

fn read(filename: &str) -> Vec<String> {
    std::fs::read_to_string(filename).unwrap()
        .trim()
        .split("\n")
        .map(|s| s.to_string())
        .collect()
}
