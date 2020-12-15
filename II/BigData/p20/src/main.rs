use rand::Rng;

struct Morris {
    counters: Vec<i32>,
    rng: rand::prelude::ThreadRng,
}

impl Morris {
    fn new(k: usize, rng: rand::prelude::ThreadRng) -> Morris {
        Morris {
            counters: vec![1; k],
            rng,
        }
    }

    fn inc(&mut self, i: usize) {
        let random = self.rng.gen::<f64>();
        if random < (2.0f64).powi(-self.counters[i]) {
            self.counters[i] += 1;
        }
    }

    fn inc_all(&mut self) {
        for i in 0..self.counters.len() {
            self.inc(i)
        }
    }

    fn expected(&self) -> f64 {
        let C = self.counters.iter().fold(0, |acc, x| acc + x) / self.counters.len() as i32;
        return (2.0f64).powi(C) - 2.0;
    }
}

fn main() {
    let mut rng = rand::thread_rng();

    let min_n = 1;
    let max_n = 10001;
    let step = 1;
    let repeat = 1;
    let k = 1;

    println!("N,E,k");
    let mut ctr = Morris::new(k, rng);
    for n in (min_n..max_n).step_by(step) {
        for _ in 0..repeat {
            ctr.inc_all();
            println!(
                "{},{},{}",
                n,
                ctr.expected(),
                ctr.counters.iter().fold(0, |acc, x| acc + x) / ctr.counters.len() as i32
            )
        }
    }
}
