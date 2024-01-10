use crate::board::Board;

pub struct Frame {
    raw: Vec<u8>,
    width: u32,
    height: u32,
}

impl Frame {
    pub fn new(width: u32, height: u32) -> Frame {
        let raw = vec![0_u8; (width * height * 3) as usize];
        Frame { raw, width, height }
    }

    pub fn render(&mut self, board: &Board) -> &[u8] {
        for y in 0..self.height {
            for x in 0..self.width {
                let index = (y as usize * self.width as usize + x as usize) * 3;
                let value = if board.get(x as i32, y as i32) { 255 } else { 0 };

                self.raw[index] = value;
                self.raw[index + 1] = value;
                self.raw[index + 2] = value;
            }
        }

        &self.raw
    }
}
