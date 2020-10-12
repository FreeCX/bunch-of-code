use std::ops::Add;

struct Sequence<T> {
    i0: T,
    i1: T,
}

impl<T> Sequence<T> {
    fn new(i0: T, i1: T) -> Sequence<T> {
        Sequence { i0, i1 }
    }
}

impl<T> Iterator for Sequence<T>
where
    T: Add<Output = T> + Copy,
{
    type Item = T;

    fn next(&mut self) -> Option<Self::Item> {
        let next = self.i1 + self.i0;
        self.i0 = self.i1;
        self.i1 = next;
        Some(next)
    }
}

fn main() {
    let (i0, i1) = (0, 1);
    let fib: Sequence<_> = Sequence::new(i0, i1);
    
    print!("{} {} ", i0, i1);
    for item in fib.take(10) {
        print!("{} ", item);
    }
    println!();
}
