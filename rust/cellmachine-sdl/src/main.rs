use sdl2::event::Event;
use sdl2::keyboard::Keycode;
use sdl2::mouse::MouseButton;
use sdl2::pixels::Color;
use sdl2::rect::Rect;

use crate::board::Board;

mod board;

fn board_next_step(board: &mut Board) {
    board.next(|f, x, y| {
        // f.get(x - 1, y - 1) ^ f.get(x - 1, y + 1)
        // f.get(x, y) ^ f.get(x - 1, y) & f.get(x, y - 1) | f.get(x + 1, y)
        // f.get(x - 1, y - 1) ^ f.get(x + 1, y - 1) ^ f.get(x - 1, y + 1) ^ f.get(x + 1, y + 1)
        // f.get(x - 1, y - 1) & f.get(x + 1, y - 1) | f.get(x - 1, y + 1) ^ f.get(x + 1, y + 1)
        // f.get(x - 1, y) ^ f.get(x + 1, y) ^ f.get(x, y - 1) ^ f.get(x, y + 1) | f.get(x, y)
        // f.get(x - 1, y) | f.get(x + 1, y) ^ f.get(x, y - 1) ^ f.get(x, y + 1) ^ f.get(x, y)
        f.get(x - 1, y) | f.get(x + 1, y) ^ f.get(x, y - 1) ^ f.get(x, y + 1) & f.get(x, y)
    });
}

fn main() {
    let fps = 30;
    let board_width: i32 = 100;
    let board_height: i32 = 100;
    let kw: i32 = 8;
    let kh: i32 = 8;
    let window_width = (kw * board_width) as u32;
    let window_height = (kh * board_height) as u32;

    let sdl_context = sdl2::init().unwrap();
    let video_subsystem = sdl_context.video().unwrap();
    let window =
        video_subsystem.window("cellmachine", window_width, window_height).position_centered().build().unwrap();
    let mut timer = sdl_context.timer().unwrap();
    let mut last_time = timer.ticks();
    let mut canvas = window.into_canvas().build().unwrap();

    let mut board = Board::new(board_width, board_height);
    let mut render_next_iter = false;
    let mut draw_mode_one = false;

    let mut event_pump = sdl_context.event_pump().unwrap();
    'running: loop {
        canvas.set_draw_color(Color::RGB(0, 0, 0));
        canvas.clear();
        canvas.set_draw_color(Color::RGB(255, 255, 255));
        let rects: Vec<_> = board
            .items()
            .iter()
            .map(|&(x, y)| Rect::new(x * kw, y * kh, kw as u32, kh as u32))
            .collect();
        let _ = canvas.fill_rects(rects.as_slice());
        canvas.present();

        for event in event_pump.poll_iter() {
            match event {
                Event::Quit { .. } | Event::KeyDown { keycode: Some(Keycode::Escape), .. } => break 'running,
                Event::KeyDown { keycode: Some(Keycode::Space), .. } => render_next_iter = !render_next_iter,
                Event::KeyDown { keycode: Some(Keycode::Right), .. } => board_next_step(&mut board),
                Event::KeyDown { keycode: Some(Keycode::R), .. } => board.clear(),
                Event::MouseMotion { x, y, .. } => {
                    if draw_mode_one {
                        board.set(x / kw, y / kh);
                    }
                }
                Event::MouseButtonUp { mouse_btn: MouseButton::Left, .. } => draw_mode_one = false,
                Event::MouseButtonDown { mouse_btn: MouseButton::Left, x, y, .. } => {
                    board.set(x / kw, y / kh);
                    draw_mode_one = true;
                }
                _ => {}
            }
        }

        if render_next_iter {
            board_next_step(&mut board);
        }

        // fps counter
        let current_time = timer.ticks();
        let elapsed = current_time - last_time;
        last_time = current_time;

        // sleep
        let sleep_time = if elapsed < 1000 / fps { 1000 / fps - elapsed } else { 1000 / fps };
        if sleep_time > 0 {
            timer.delay(sleep_time);
        }
    }
}
