#[derive(Debug, Clone, Copy)]
pub struct Rnd {
    init: u32
}

impl Rnd {
    pub fn new(init: u32) -> Rnd {
        Rnd { init }
    }

    pub fn next(&mut self) -> u32 {
        self.init ^= self.init << 17;
        self.init ^= self.init >> 5;
        self.init ^= self.init << 13;
        self.init
    }

    pub fn in_range(&mut self, min: u32, max: u32) -> u32 {
        self.next() % (max - min) + min
    }

    pub fn mult2(&mut self, min: u32, max: u32) -> u32 {
        let v = self.in_range(min, max);
        if v % 2 != 0 { v - 1 } else { v }
    }
}