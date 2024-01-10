use std::mem;

pub struct Board {
    // current state
    cell: Vec<bool>,
    // for new state
    buffer: Vec<bool>,
    width: i32,
    height: i32,
}

impl Board {
    pub fn new(width: i32, height: i32) -> Board {
        let cell = vec![false; width as usize * height as usize];
        let buffer = cell.clone();
        Board { cell, buffer, width, height }
    }

    pub fn set(&mut self, x: i32, y: i32) {
        if x >= 0 && y >= 0 && x < self.width && y < self.height {
            self.cell[(y * self.width) as usize + x as usize] = true;
        }
    }

    pub fn get(&self, x: i32, y: i32) -> bool {
        if x >= 0 && y >= 0 && x < self.width && y < self.height {
            self.cell[(y * self.width) as usize + x as usize]
        } else {
            false
        }
    }

    // TODO: improve it
    pub fn items(&self) -> Vec<(i32, i32)> {
        let mut result = Vec::new();
        for y in 0..self.height {
            for x in 0..self.width {
                if self.cell[(y * self.width) as usize + x as usize] {
                    result.push((x, y));
                }
            }
        }
        result
    }

    pub fn clear(&mut self) {
        for item in self.cell.iter_mut() {
            *item = false;
        }
    }

    // calculating the next state of the board using rule
    pub fn next<R>(&mut self, rule: R)
    where
        R: Fn(&Board, i32, i32) -> bool,
    {
        for y in 0..self.height {
            for x in 0..self.width {
                // calculate new sate
                self.buffer[(y * self.width) as usize + x as usize] = rule(self, x, y);
            }
        }
        // swap current and new state
        mem::swap(&mut self.cell, &mut self.buffer);
    }
}
