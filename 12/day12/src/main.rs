use std::collections::HashMap;

fn main() {
    let filename = std::env::args().skip(1).next().unwrap();
    let mut records = read(&filename);

    records = multiply(&records, 5);


    let mut count: usize = 0;
    for (pattern, strips) in records {
        let mut cache = HashMap::<(usize, String, Vec<usize>), usize>::new();

        let ways = look(0, &pattern, &strips, &mut cache);
        println!("{}, {:?}, {} ways", pattern, strips, ways);
        count += ways;
    }
    println!("{}", count);
}

fn read(filename: &str) -> Vec<(String, Vec<usize>)> {
    std::fs::read_to_string(filename).unwrap()
        .lines()
        .map(|s| {
            let tokens: Vec<&str> = s.split(' ').collect();
            let strips: Vec<usize> = tokens[1]
                .split(',')
                .map(|v| {
                    v.parse::<usize>().unwrap()
                })
                .collect();
            (tokens[0].to_string(), strips)
        })
        .collect()
}

fn look(matching: usize, pattern: &str, strips: &[usize], cache: &mut HashMap<(usize, String, Vec<usize>), usize>) -> usize {
    let h = (matching, String::from(pattern), Vec::from(strips));
    if cache.contains_key(&h) {
        return *cache.get(&h).unwrap();
    }

    let count: usize;
    if strips.len() > 0 {
        if pattern.len() > 0 {
            let c = pattern.chars().next().unwrap();
            match c {
                '.' => {
                    if strips[0] == matching {
                        count = look(0, &pattern[1..], &strips[1..], cache);
                    } else if matching == 0 {
                        count = look(0, &pattern[1..], strips, cache);
                    } else {
                        count = 0;
                    }
                },
                '#' => {
                    if strips[0] > matching {
                        count = look(matching + 1, &pattern[1..], strips, cache);
                    } else {
                        count = 0;
                    }
                },
                '?' => {
                    let count1;
                    let count2;

                    // ? -> #
                    if strips[0] > matching {
                        count1 = look(matching + 1, &pattern[1..], strips, cache);
                    } else {
                        count1 = 0;
                    }

                    // ? -> .
                    if strips[0] == matching {
                        count2 = look(0, &pattern[1..], &strips[1..], cache);
                    } else if matching == 0 {
                        count2 = look(0, &pattern[1..], strips, cache);
                    } else {
                        count2 = 0;
                    }
                    count = count1 + count2;
                },
                _ => {
                    panic!("should not be here");
                }
            }
        } else {
            if matching == strips[0] {
                count = look(0, pattern, &strips[1..], cache);
            } else if matching < strips[0] {
                count = 0;
            } else {
                panic!("should not be here");
            }
        }
    } else {
        if pattern.len() > 0 {
            let c = pattern.chars().next().unwrap();
            match c {
                '.' => {
                    count = look(matching, &pattern[1..], strips, cache);
                },
                '#' => {
                    count = 0;
                },
                '?' => {
                    count = look(matching, &pattern[1..], strips, cache);
                },
                _ => {
                    panic!("should not be here");
                }
            }
        } else {
            count = 1;
        }
    }

    cache.insert(h, count);
    count
}

fn multiply(records: &Vec<(String, Vec<usize>)>, multiple: usize) -> Vec<(String, Vec<usize>)> {
    records.iter()
        .map(|(pattern, strips)| {
            let mut p = pattern.clone();
            p.push('?');
            p = p.repeat(multiple - 1);
            p.push_str(pattern);
            (p, strips.clone().repeat(multiple))
        })
        .collect()
}
