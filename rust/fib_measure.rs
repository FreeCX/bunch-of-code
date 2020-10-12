use std::time::SystemTime;

fn measure<F>(name: &str, value: usize, f: F) where F: Fn(usize) -> usize {
    let start = SystemTime::now();
    let result = f(value);
    let elapsed = start.elapsed().unwrap();
    println!("{} with value {} return {} during {:?}", name, value, result, elapsed);
}

fn fib_cache(n: usize) -> usize {
    let mut cache = vec![0; n + 1];
    return fib_memo(&mut cache, n);

    fn fib_memo(cache: &mut Vec<usize>, n: usize) -> usize {
        if n == 0 || n == 1 {
            return 1;
        }
        if cache[n] == 0 {
            cache[n] = fib_memo(cache, n - 1) + fib_memo(cache, n - 2);
        }
        cache[n]
    }
}

fn fib_classic(n: usize) -> usize {
    match n {
        0 | 1 => 1,
        _ => fib_classic(n - 1) + fib_classic(n - 2)
    }
}

fn fib_iterate(n: usize) -> usize {
    let mut a = 0;
    let mut b = 1;
    
    for _ in 0..n {
        let c = a + b;
        a = b;
        b = c;
    }
    b
}

fn main() {
    const N: usize = 40;
    
    measure("classic", N, fib_classic);
    measure(" cached", N, fib_cache);
    measure("iterate", N, fib_iterate);
}

