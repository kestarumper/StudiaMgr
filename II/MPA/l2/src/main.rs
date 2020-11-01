use csv::Writer;
use rand::seq::SliceRandom;
use std::error::Error;

#[derive(Debug)]
struct Permutation {
    nums: Vec<usize>,
    cycles: Vec<Vec<usize>>,
    static_points: usize,
    records: usize,
}

impl Permutation {
    fn get_random_permutation(n: usize) -> Vec<usize> {
        let mut rng = rand::thread_rng();
        let mut nums: Vec<usize> = (0..n).collect();
        nums.shuffle(&mut rng);
        return nums;
    }

    fn serialize(&self) -> Vec<usize> {
        vec![
            self.nums.len(),
            self.static_points,
            self.cycles.len(),
            self.records,
        ]
    }

    fn new(n: usize) -> Permutation {
        let nums = Permutation::get_random_permutation(n);
        let mut indices: Vec<usize> = Vec::new();
        let mut cycles: Vec<Vec<usize>> = Vec::new();
        let mut static_points = 0;
        let mut records = 0;

        let mut last_max = 0;
        for (i, num) in nums.iter().enumerate() {
            if *num >= last_max {
                last_max = *num;
                records += 1;
            }

            if indices.contains(&i) {
                continue;
            }
            let mut cycle: Vec<usize> = vec![i];
            let mut next = i;
            loop {
                next = nums[next];
                if next == i {
                    break;
                }
                cycle.push(next);
                indices.push(next);
            }
            if cycle.len() == 1 {
                static_points += 1;
            }
            cycles.push(cycle);
        }

        Permutation {
            nums,
            cycles,
            static_points,
            records,
        }
    }
}

fn main() {
    let min_perm_len = 100;
    let max_perm_len = 10001;
    let step = 100;
    let repeat = 1000;

    let path = "result.csv";
    let mut wtr = Writer::from_path(path).unwrap();

    for perm_len in (min_perm_len..max_perm_len).step_by(step) {
        for _ in 0..repeat {
            let perm = Permutation::new(perm_len);
            let serialized = perm.serialize();
            wtr.serialize(serialized).unwrap();
        }
        wtr.flush().unwrap();
        println!("💾 {:?}", perm_len)
    }
}
