use std::time;
use std::env;

struct Rnd {
    init: u32
}

struct PGen {
    alphabet: String,
    generator: Rnd
}

impl Rnd {
    fn new(init: u32) -> Rnd {
        Rnd { init }
    }

    fn next(&mut self) -> u32 {
        self.init ^= self.init << 17;
        self.init ^= self.init >> 5;
        self.init ^= self.init << 13;
        self.init
    }

    fn in_range(&mut self, min: u32, max: u32) -> u32 {
        self.next() % (max - min) + min
    }
}

impl PGen {
    fn new(generator: Rnd, alphabet: String) -> PGen {
        PGen { generator, alphabet }
    }

    fn generate(&mut self, length: u32) -> String {
        (0..length).map(|_| {
            let index = self.generator.in_range(0, self.alphabet.len() as u32);
            self.alphabet.chars().skip(index as usize).next().unwrap()
        }).collect()
    }

    fn iterate(mut self, length: u32) -> impl Iterator<Item = String> {
        std::iter::repeat_with(move || self.generate(length))
    }
}

fn init_value() -> u32 {
    match time::SystemTime::now().duration_since(time::SystemTime::UNIX_EPOCH) {
        Ok(value) => value.as_secs() as u32,
        Err(_) => 42
    }
}

fn main() {
    let arguments: Vec<_> = env::args().into_iter().collect();
    let mut length = 8;
    let mut count = 10;

    if arguments.len() == 2 {
        count = arguments[1].parse().unwrap();
    }
    else if arguments.len() == 3 {
        count = arguments[1].parse().unwrap();
        length = arguments[2].parse().unwrap();
    }
    else {
        println!("usage: {} <count> <length>\nuse default value of length ({}) and count ({})\n", arguments[0], length, count);
    }

    let alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890".to_owned();
    let generator = Rnd::new(init_value());
    let pgen = PGen::new(generator, alphabet);
    
    for item in pgen.iterate(length).take(count) {
        println!("{}", item);
    }
}