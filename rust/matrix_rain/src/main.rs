extern crate rustty;

mod rain;
mod rnd;

use rustty::{Terminal, Event};
use std::time::Duration;
use std::thread::sleep;
use rain::Rain;
use rnd::Rnd;
use std::fs;

fn main() {
    let filename = "alphabet.txt";
    // читаем наш алфавит символов из файла или используем дефолтный
    let alphabet = match fs::read_to_string(filename) {
        Ok(value) => value,
        Err(err) => {
            eprintln!("[warn] use default alphabet: {} [{}]", err, filename);
            "abcdefghijklmnopqrstuvwxyz".to_owned()
        }
    };

    // инициализируем терминал, генератор и дождь
    let mut term = Terminal::new().unwrap();
    let rnd = Rnd::new(42);
    let size = (term.cols() as u32 - 1, term.rows() as u32 - 1);
    let mut rain = Rain::new(rnd, size, 100, &alphabet);

    // вспомогательные переменные по скорости работы
    let sleep_time = Duration::new(0, 50_000_000);
    let dur = Duration::new(0, 10_000_000);

    // основной цикл
    'main: loop {
        // обработка клавиш
        while let Ok(Some(Event::Key(ch))) = term.get_event(dur) {
            match ch {
                'q' => break 'main,
                _ => {}
            }
        }
        // перерисовываем
        rain.update(&mut term, size);
        // спим
        sleep(sleep_time);
    }
}
