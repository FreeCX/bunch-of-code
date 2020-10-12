use std::io::Write;
use std::io;

fn calc_speed(temperature: f32) -> f32 {
    let (k, na, g, m) = (1.3806488, 6.02214129, 1.40, 29.98E-3);
    (g * k * na * temperature / m).sqrt()
}

fn read_float() -> f32 {
    let mut buffer = String::new();
    match io::stdin().read_line(&mut buffer) {
        Err(err) => panic!("IO problem ({})", err),
        _ => ()
    };
    let trimmed_data = buffer.trim();
    match trimmed_data.parse::<f32>() {
        Ok(value) => value,
        Err(err) => panic!("problem with parsing `{}` value ({})", trimmed_data, err)
    }
}

fn print_flush(string: &str) {
    print!("{}", string);
    match io::stdout().flush() {
        Err(err) => panic!("IO problem ({})", err),
        _ => ()
    }
}

fn main() {
    let shift_to_kelvin: f32 = 273.15;

    print_flush("Введите температуру на улице (градусы цельсия): ");
    let temperature = read_float() + shift_to_kelvin;
    print_flush("Введите прошедшее время от вспышки до грома (сек): ");
    let elapsed_time = read_float();

    let velocity = calc_speed(temperature);
    let distance = velocity * elapsed_time;
    
    println!("Скорость звука в воздухе ~ {:.2E} м/с\nРасстояние до точки попадания молнии ~ {:.2E} м",
             velocity, distance);
}