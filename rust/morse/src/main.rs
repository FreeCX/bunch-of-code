#![allow(dead_code)]
#[macro_use]
extern crate lazy_static;

use std::collections::HashMap;
use std::fs::File;
use std::io::Write;

lazy_static! {
    // спец. коды
    static ref ERROR_CODE: &'static str = "········";
    static ref END_TRANSMISSION: &'static str = "··-·-";
    // таблица кодов
    static ref MORSE_TABLE: Vec<(&'static str, &'static str)> = vec![
        ("А", "·-"), ("Б", "-···"), ("В", "·--"), ("Г", "--·"), ("Д", "-··"), ("Ё", "·"), ("Е", "·"),
        ("Ж", "···-"), ("З", "--··"), ("И", "··"), ("Й", "·---"), ("К", "-·-"), ("Л", "·-··"), ("М", "--"),
        ("Н", "-·"), ("О", "---"), ("П", "·--·"), ("Р", "·-·"), ("С", "···"), ("Т", "-"), ("У", "··-"),
        ("Ф", "··-·"), ("Х", "····"), ("Ц", "-·-·"), ("Ч", "---·"), ("Ш", "----"), ("Щ", "--·-"),
        ("Ъ", "--·--"), ("Ы", "-·--"), ("Ь", "-··-"), ("Э", "··-··"), ("Ю", "··--"), ("Я", "·-·-"),
        ("1", "·----"), ("2", "··---"), ("3", "···--"), ("4", "····-"), ("5", "·····"), ("6", "-····"),
        ("7", "--···"), ("8", "---··"), ("9", "----·"), ("0", "-----"), (".", "······"), (",", "·-·-·-"),
        (":", "---···"), (";", "-·-·-·"), (")", "-·--·-"), ("(", "-·--·-"), ("'", "·----·"), ("\"", "·-··-·"),
        ("-", "-····-"), ("\\", "-··-·"), ("/", "-··-·"), ("!", "··--··"),  ("?", "--··--"), (" ", "-···-"),
        ("@", "·--·-·")
    ];
    // генерируем словарь
    static ref CODER: HashMap<String, String> = {
        let mut hashmap = HashMap::new();
        for &(symbol, morse) in MORSE_TABLE.iter() {
            hashmap.insert(symbol.to_string(), morse.to_string());
        }
        hashmap
    };
}

// функция кодирования
fn encode(input: &str) -> String {
    let mut result = String::new();
    // перегоняем текст в ЗАГЛАВНЫЙ формат
    let input_str = input.to_uppercase();
    for symbol in input_str.chars() {
        match CODER.get(&format!("{}", symbol)) {
            // кодируем символ
            Some(code) => result.push_str(&format!("{} ", code)),
            // игнорим
            None => (),
        };
    }
    // добавляем индификатор конца трансляции
    result.push_str(&END_TRANSMISSION);
    result
}

fn generate(freq: f32, duration: f32, volume: f32) -> Vec<u8> {
    // частота дискретизации
    let sample_rate = 44100.0;
    // amplitude = 2^16 * volume
    let amplitude = std::i16::MAX as f32 * volume;
    // количество генерируемых сэмплов
    let total_samples: u32 = (sample_rate * duration).round() as u32;
    // угловая частота / частоте дискретизации
    let w = std::f32::consts::TAU * freq / total_samples as f32;
    // мы будем делать u16, а записывать по 2 блока u8 в формате BigEndian
    let mut buffer: Vec<u8> = Vec::with_capacity(2 * total_samples as usize);
    for k in 0..total_samples {
        // f = A * sin(kw)
        // A -- амплитуда сигнала
        // k -- номер сэмпла
        let sample = (amplitude * (k as f32 * w).sin()) as i16;
        // проталкиваем в буффер
        buffer.extend_from_slice(&sample.to_le_bytes());
    }
    buffer
}

fn main() {
    let mut file = File::create("./generated.sound").expect("can't create file!");
    // длительность звучания 'точки'
    let dot_len = 0.15;
    // вектор для наших сэмплов
    let mut result_audio: Vec<u8> = Vec::new();
    // звук одной 'точки'
    let dot = generate(300.0, dot_len, 1.0);
    // и соответственно 'тире'
    let dash = generate(300.0, 3.0 * dot_len, 1.0);
    // собираем 44100 * 3 * dot_len нулей (u16 или по два для u8) для паузы между знаками
    let e_pause = vec![0_u8; 2 * (44100.0 * 3.0 * dot_len).round() as usize];
    // собираем 44100 * 7 * dot_len нулей для паузы между словами
    let w_pause = vec![0_u8; 2 * (44100.0 * 7.0 * dot_len).round() as usize];
    // кодируем наш текст
    let morse_text = encode("привет мир!");
    println!("{}", morse_text);
    for code in morse_text.chars() {
        match code {
            '·' => result_audio.extend(dot.clone()),
            '-' => result_audio.extend(dash.clone()),
            // пауза между словами
            ' ' => {
                result_audio.extend(w_pause.clone());
                continue;
            }
            _ => {}
        };
        // пауза между символами
        result_audio.extend(e_pause.clone());
    }
    file.write_all(result_audio.as_slice()).unwrap();
}
