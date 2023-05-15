fn xor_shift(mut init: u32) -> impl Iterator<Item = u32> {
    std::iter::repeat_with(move || {
        init ^= init << 13;
        init ^= init >> 17;
        init ^= init << 5;
        init
    })
}

fn main() {
    for i in xor_shift(42).take(10) {
        print!("{} ", i);
    }
}
