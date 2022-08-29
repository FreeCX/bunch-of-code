// struct serialize-deserialize demo

use std::convert::TryInto;

trait Serialize {
    fn to_bytes(&self) -> ObjectData;
}

trait Deserialize {
    fn from_bytes(data: ObjectData) -> Self
    where
        Self: Sized;
}

struct Serializer {
    data: Vec<ObjectData>,
}

type ObjectData = Vec<u8>;

#[derive(Debug)]
struct Foo {
    a: u16,
    b: u8,
}

#[derive(Debug)]
struct Bar {
    a: u8,
}

impl Serializer {
    fn new() -> Self {
        Serializer { data: Vec::new() }
    }

    fn push<S: Serialize>(&mut self, data: S) {
        self.data.push(data.to_bytes());
    }

    fn pop<D: Deserialize>(&mut self) -> D {
        let item = self.data.pop().unwrap();
        D::from_bytes(item)
    }

    fn serialize(&self) -> ObjectData {
        let mut result = ObjectData::new();
        for item in &self.data {
            let size = (item.len() as u32).to_le_bytes();
            dbg!(size);
            result.extend(size);
            result.extend(item);
        }
        result
    }

    fn deserialize(bytes: ObjectData) -> Self {
        let total_bytes = bytes.len();
        dbg!(total_bytes);
        let mut index = 0;
        let mut data = Vec::new();
        while index < total_bytes {
            let size = u32::from_le_bytes(bytes[index + 0..index + 4].try_into().unwrap()) as usize;
            dbg!(size);
            let block = Vec::from(&bytes[index + 4..index + 4 + size]);
            dbg!(&block);
            data.push(block);
            dbg!(index);
            index += 4 + size;
        }
        Serializer { data }
    }
}

impl Serialize for Foo {
    fn to_bytes(&self) -> ObjectData {
        let mut result = ObjectData::new();
        result.extend(self.a.to_le_bytes());
        result.extend(self.b.to_le_bytes());
        result
    }
}

impl Serialize for Bar {
    fn to_bytes(&self) -> ObjectData {
        vec![self.a]
    }
}

impl Deserialize for Foo {
    fn from_bytes(data: ObjectData) -> Self {
        dbg!(&data);
        Foo {
            a: u16::from_le_bytes(data[0..2].try_into().unwrap()),
            b: data[2],
        }
    }
}

impl Deserialize for Bar {
    fn from_bytes(data: ObjectData) -> Self {
        dbg!(&data);
        Bar { a: data[0] }
    }
}

fn main() {
    let foo1 = Foo { a: 1024, b: 42 };
    let bar1 = Bar { a: 34 };

    println!("foo = {:?}", foo1);
    println!("bar = {:?}", bar1);

    let mut s = Serializer::new();
    s.push(foo1);
    s.push(bar1);
    let r = s.serialize();

    println!("serialized = {:?}", r);

    let mut s = Serializer::deserialize(r);
    let bar2: Bar = s.pop();
    let foo2: Foo = s.pop();

    println!("foo = {:?}", foo2);
    println!("bar = {:?}", bar2);
}
