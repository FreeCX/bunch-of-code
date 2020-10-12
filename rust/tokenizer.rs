#[derive(Debug, Eq, PartialEq)]
enum TokenType {
    // [a-zA-Z]+
    Id,
    // [0-9]+
    Number,
    // \s
    Space,
    // [](){}<>
    Bracket,
    // +-*/%^=
    Operator,
    // ...
    Reserved
}

#[derive(Debug)]
struct Tokenizer<'a> {
    input: &'a str,
    last_type: TokenType,
    last_pos: usize,
}

impl<'a> Tokenizer<'a> {
    fn new(input: &'a str) -> Tokenizer<'a> {
        Tokenizer {
            input,
            last_type: TokenType::Reserved,
            last_pos: 0
        }
    }
}

// Кривая реализация токенизирующей функции
impl<'a> Iterator for Tokenizer<'a> {
    type Item = &'a str;

    fn next(&mut self) -> Option<Self::Item> {
        for (mut index, character) in self.input[self.last_pos ..].chars().enumerate() {
            // делаем сдвиг на последнюю просмотренную позицию
            index += self.last_pos;
            // определяем тип для текущего символа
            let curr_type = check_type(character);
            // условие разделения на токены
            let split_condition = curr_type != self.last_type || curr_type == self.last_type && curr_type == TokenType::Bracket;
            // разделяем все типы
            if split_condition {
                // выбираем из данных текущий токен
                let curr_token = self.input[self.last_pos .. index].trim();
                // если токен не пустой и прошлый не пробел
                if curr_token.len() > 0 && self.last_type != TokenType::Space {
                    // обновляяем позицию
                    self.last_pos = index;
                    // возвращаем токен
                    return Some(curr_token);
                }
            }
            // обновляем последний токен
            self.last_type = curr_type;
        }
        // возвращаем последний элемент
        if self.input.len() - self.last_pos != 0 {
            let curr_token = self.input[self.last_pos ..].trim();
            self.last_pos = self.input.len();
            return Some(curr_token);
        }
        None
    }
}

fn check_type(token: char) -> TokenType {
    match token {
        '[' | ']' | '(' | ')' | '{' | '}' | '<' | '>' => TokenType::Bracket,
        '+' | '-' | '*' | '/' | '%' | '^' | '=' => TokenType::Operator,
        'A' ..= 'Z' | 'a' ..= 'z' => TokenType::Id,
        '0' ..= '9' | '.' => TokenType::Number,
        ' ' => TokenType::Space,
        _ => unimplemented!()
    }
}

fn main() {
    let data = "(+ 1 2 3.14 (* 10 20 30) (sin 30))";
    print!("data = `{}`\ntokens = ", data);
    for item in Tokenizer::new(data) {
        print!("'{}' ", item);
    }
}
