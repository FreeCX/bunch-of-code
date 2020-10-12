#[macro_use]
extern crate image_loader as il;
use std::io::prelude::*;
use std::io::BufReader;
use std::process::exit;
use std::io::stdout;
use std::fs::File;
use std::env;

fn linear_gradient(c1: il::Color, c2: il::Color, n: u16) -> Vec<il::Color> {
    let mut colors = Vec::new();
    for i in 1..n {
        let t = i as f32 / (n - 1) as f32;
        let r = ((1.0 - t) * c1.red as f32 + t * c2.red as f32) as u8;
        let g = ((1.0 - t) * c1.green as f32 + t * c2.green as f32) as u8;
        let b = ((1.0 - t) * c1.blue as f32 + t * c2.blue as f32) as u8;
        colors.push(color!(r, g, b));
    }
    colors
}

fn polylinear_gradient(colors: Vec<il::Color>, n: u16) -> Vec<il::Color> {
    let mut res_colors = vec![colors[0]];
    let n_out = ((n as f32) / (colors.len() - 1) as f32).ceil() as u16;
    for (c1, c2) in colors.iter().zip(colors.iter().skip(1)) {
        res_colors.extend(linear_gradient(*c1, *c2, n_out));
        res_colors.push(*c2);
    }
    res_colors
}

fn main() {
    // select input & output file
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Heatmap Drawer\nusage: {} <filename>", args[0]);
        exit(-1);
    }

    let input_file = args[1].clone();
    let output_file = args[1].clone() + ".tga";

    // prepare gradients
    let colors = vec![
        color!(12, 7, 134),
        color!(182, 47, 139),
        color!(244, 137, 71),
        color!(239, 248, 33),
    ];
    let gradient = polylinear_gradient(colors, 255);
    println!("[+] create {} gradient colors ... DONE", gradient.len());

    // load & rescale
    let file = File::open(&input_file).unwrap();
    let file = BufReader::new(file);
    let mut l_matrix: Vec<Vec<f32>> = Vec::new();
    let mut max_value = 0_f32;
    print!("[+] loading `{}' file ... ", input_file);
    stdout().flush().expect("Can't flush to stdout");
    
    for line in file.lines() {
        match line {
            Ok(value) => {
                let v = value.split_whitespace().map(|x| x.parse::<f32>().unwrap()).collect::<Vec<f32>>();
                let new_max = v.iter().fold(0_f32, |m, &c| m.max(c));
                max_value = max_value.max(new_max);
                l_matrix.push(v);
            },
            Err(_) => (),
        };
    }
    print!("DONE\n[+] rescaling data ... ");
    stdout().flush().expect("Can't flush to stdout");

    let matrix: Vec<Vec<u8>> = l_matrix.iter().map(|x| {
        x.iter().map(|&x| {
            ((x / max_value) * 255.0).round() as u8
        }).collect()
    }).collect();
    print!("DONE\n[+] image reconstruction ... ");
    stdout().flush().expect("Can't flush to stdout");

    // draw & save
    let mut img = il::TGAImage::new(matrix[0].len() as u16, matrix.len() as u16).unwrap();
    for (y, line) in matrix.iter().enumerate() {
        for (x, item) in line.iter().enumerate() {
            img.set(x as u16, y as u16, gradient[*item as usize]);
        }
    }
    print!("DONE\n[+] save to `{}' file ... ", output_file);
    stdout().flush().expect("Can't flush to stdout");
    
    img.flip_horizontally();
    img.write_to_file(output_file);
    println!("DONE");
}
