// implement Xoshiro256**
// url: http://prng.di.unimi.it/

struct State {
    s0: u64,
    s1: u64,
    s2: u64,
    s3: u64
}

fn rotl(x: u64, k: i32) -> u64 {
    (x << k) | (x >> (64 - k))
}

impl State {
    fn new(seed: [u64; 4]) -> State {
        State {
            s0: seed[0],
            s1: seed[1],
            s2: seed[2],
            s3: seed[3],
        }
    }

    fn next(&mut self) -> u64 {
        let result = rotl(self.s1.overflowing_mul(5).0, 7).overflowing_mul(9).0;
        let t = self.s1 << 17;

        self.s2 ^= self.s0;
        self.s3 ^= self.s1;
        self.s1 ^= self.s2;
        self.s0 ^= self.s3;

        self.s2 ^= t;
        self.s3 = rotl(self.s3, 45);

        result
    }
}

fn main() {
    let mut g = State::new([0x180ec6d33cfd0aba, 0xd5a61266f0c9392c, 0xa9582618e03fc9aa, 0x39abdc4529b1661c]);
    for _ in 0..10 {
        println!("state: {}", g.next());
    }
}