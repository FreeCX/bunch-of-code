#[macro_use]
extern crate lazy_static;
extern crate iced;

use iced::{
    button, executor, text_input, Align, Application, Button, Clipboard, Column, Command, Container, Element,
    HorizontalAlignment, Length, Row, Settings, Text,
};
use std::collections::HashMap;

lazy_static! {
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
        ("@", "·--·-·"),
        ("A", "·-"), ("B", "-···"), ("C", "-·-·"), ("D", "-··"), ("E", "."), ("F", "··-·"), ("G", "--·"),
        ("H", "····"), ("I", "··"), ("J", "·---"), ("K", "-·-"), ("L", "·-··"), ("M", "--"), ("N", "-·"),
        ("O", "---"), ("P", "---"), ("P", "·--·"), ("Q", "--·-"), ("R", "·-·"), ("S", "···"), ("T", "-"),
        ("U", "··-"), ("V", "···-"), ("W", "·--"), ("X", "-··-"), ("Y", "-·--"), ("Z", "--··")
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
    result
}

#[derive(Default)]
struct Window {
    input: String,
    output: String,
    input_state: text_input::State,
    button_state: button::State,
}

#[derive(Debug, Clone)]
pub enum Message {
    InputChanged(String),
    ClipboardCopy,
}

impl Application for Window {
    type Executor = executor::Default;
    type Message = Message;
    type Flags = ();

    fn new(_flags: ()) -> (Self, Command<Message>) {
        (Self::default(), Command::none())
    }

    fn title(&self) -> String {
        format!("Morse Code Generator")
    }

    fn update(&mut self, message: Message, clipboard: &mut Clipboard) -> Command<Message> {
        match message {
            Message::InputChanged(input) => {
                self.output = encode(&input);
                self.input = input;
            }
            Message::ClipboardCopy => clipboard.write(self.output.clone()),
        }

        Command::none()
    }

    fn view(&mut self) -> Element<Message> {
        let title = Text::new("Генератор кода Морзе").size(50).color([0.5, 0.5, 0.5]);

        let input = text_input::TextInput::new(
            &mut self.input_state,
            "Введите сюда текст...",
            &self.input,
            Message::InputChanged,
        )
        .size(20)
        .padding(20);

        let button = Button::new(
            &mut self.button_state,
            Text::new("Скопировать").horizontal_alignment(HorizontalAlignment::Center),
        )
        .on_press(Message::ClipboardCopy)
        .min_width(10)
        .padding(20);

        let output = Text::new(&self.output).size(30).color([0.5, 0.5, 0.5]);

        let content = Column::new()
            .width(Length::Units(700))
            .spacing(20)
            .align_items(Align::Center)
            .push(title)
            .push(Row::new().spacing(20).push(input).push(button))
            .push(output);

        Container::new(content).width(Length::Fill).height(Length::Fill).padding(20).center_x().center_y().into()
    }
}

pub fn main() -> iced::Result {
    Window::run(Settings::default())
}
