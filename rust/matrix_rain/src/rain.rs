use rustty::{Terminal, Color};
use crate::rnd::Rnd;

#[derive(Clone, Copy)]
struct Line {
    last_char: char,
    next_char: char,
    last: u32,
    next: u32,
    x: u32
}

#[derive(Clone, Copy)]
struct Eraser {
    x: u32,
    y: u32
}

pub struct Rain {
    rnd: Rnd,
    lines: Vec<Line>,
    erasers: Vec<Eraser>,
    alphabet: Vec<char>,
}

impl Line {
    fn new(start_x: u32, start_y: u32) -> Line {
        Line {
            last_char: ' ',
            next_char: ' ',
            last: start_y,
            next: start_y,
            x: start_x
        }
    }
}

impl Eraser {
    fn new(start_x: u32, start_y: u32) -> Eraser {
        Eraser {
            x: start_x,
            y: start_y
        }
    }
}

impl Rain {
    pub fn new(mut rnd: Rnd, size: (u32, u32), count: usize, alphabet: &str) -> Rain {
        let mut lines: Vec<Line> = Vec::with_capacity(count);
        let mut erasers: Vec<Eraser> = Vec::with_capacity(count / 2);
        let (width, height) = size;
        for i in 0..count {
            let (px, py) = (rnd.mult2(1, width), rnd.mult2(1, height));
            lines.push(Line::new(px, py));
            if i % 2 == 0 {
                erasers.push(Eraser::new(px, py));
            }
        }
        Rain { rnd, lines, erasers, alphabet: alphabet.chars().collect::<Vec<char>>() }
    }

    pub fn update(&mut self, term: &mut Terminal, size: (u32, u32)) {
        let (cols, rows) = size;
        for line in self.lines.iter_mut() {
            line.last = line.next;
            line.last_char = line.next_char;
            line.next_char = self.alphabet[self.rnd.in_range(0, self.alphabet.len() as u32) as usize];
            if line.last >= rows {
                line.next = 0;
                line.x = self.rnd.mult2(1, cols);
            } else {
                line.next = line.last + 1;
            }
            if line.x >= cols {
                line.x %= cols;
            }
            term[(line.x as usize, line.next as usize)].set_fg(Color::White).set_ch(line.next_char);
            term[(line.x as usize, line.last as usize)].set_fg(Color::Green).set_ch(line.last_char);
        }
        for ers in self.erasers.iter_mut() {
            if ers.y >= rows {
                ers.y = 0;
                ers.x = self.rnd.mult2(1, cols);
            } else {
                ers.y += 1;
            }
            if ers.x >= cols {
                ers.x %= cols;
            }
            term[(ers.x as usize, ers.y as usize)].set_ch(' ');
        }
        term.swap_buffers().expect("can't swap buffers");
    }
}
