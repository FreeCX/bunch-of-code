use crate::board::Board;
use crate::ffmpeg::Render;
use crate::frame::Frame;

mod board;
mod ffmpeg;
mod frame;

fn main() {
    let width: u32 = 100;
    let height: u32 = 100;
    let scale: u32 = 3;
    let steps = 1000;
    let fps = 30;

    let mut board = Board::new(width as i32, height as i32);
    board.set(width as i32 - 1, 0);

    let mut render = Render::create("render.mp4", width, height, scale, fps);
    let mut frame = Frame::new(width, height);

    for _ in 0..steps {
        board.next(|f, x, y| f.get(x - 1, y) | f.get(x + 1, y) ^ f.get(x, y - 1) ^ f.get(x, y + 1) & f.get(x, y));
        render.append(frame.render(&board));
    }
}
