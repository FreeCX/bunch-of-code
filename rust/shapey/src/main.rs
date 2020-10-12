extern crate json;
extern crate rayon;
extern crate geo;

use geo::algorithm::contains::Contains;
use geo::{LineString, Polygon, Point};
use std::time::SystemTime;
use rayon::prelude::*;
use std::io::Write;
use std::fs;

fn load_data(file: &str) -> Result<(Vec<Point<f32>>, Vec<Polygon<f32>>), String> {
    let buffer = fs::read_to_string(file).map_err(|e| e.to_string())?;
    let data = json::parse(&buffer).map_err(|e| e.to_string())?;
    let mut points = Vec::new();

    for p in data["points"].members() {
        let x = p[0].as_f32().ok_or(String::from("problem with value parsing"))?;
        let y = p[1].as_f32().ok_or(String::from("problem with value parsing"))?;
        points.push(Point::new(x, y));
    }
    
    let mut polygons = Vec::new();
    for p in data["polygons"].members() {
        let mut poly = Vec::new();
        for c in p.members() {
            let x = c[0].as_f32().ok_or(String::from("problem with value parsing"))?;
            let y = c[1].as_f32().ok_or(String::from("problem with value parsing"))?;
            poly.push((x, y));
        }
        polygons.push(Polygon::new(LineString::from(poly), vec![]));
    }
    
    Ok((points, polygons))
}

fn main() {
    let (points, polygons) = load_data("data/result.json").unwrap();

    let now = SystemTime::now();
    
    let result: Vec<Vec<_>> = points.par_iter().map(|p| {
        let mut includes = Vec::new();
        for (jndex, polygon) in polygons.iter().enumerate() {
            if polygon.contains(p) {
                includes.push(jndex);
            }
        }
        includes
    }).collect();

    let elapsed = now.elapsed();
    println!("elapsed = {:?}", elapsed);

    let mut file = fs::File::create("result-rust.txt").unwrap();
    for (index, item) in result.iter().enumerate() {
        let _ = write!(file, "{}: {:?}\n", index, item);
    }
}
