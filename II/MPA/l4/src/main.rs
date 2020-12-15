use rand::distributions::{Distribution, Uniform};
use std::cmp;

/// # Arguments
/// * `n` - # of bins
/// * `m` - # of balls (samples)
fn experiment(n: usize, m: usize, rng: &mut rand::prelude::ThreadRng) -> [usize; 2] {
    let mut bins: Vec<usize> = vec![0; n];
    let random = Uniform::from(0..bins.len());
    
    random.sample_iter(rng).take(m).for_each(|i| bins[i] += 1);

    let result: [usize; 2] = bins.iter().fold([0, 0] as [usize; 2], |acc, x| {
        let max = cmp::max(acc[0], *x);
        let increase = if *x == 0 { 1 } else { 0 };
        [max, acc[1] + increase]
    });

    return result;
}

fn main() {
    let mut rng = rand::thread_rng();

    let min_n = 100;
    let max_n = 10001;
    let step = 100;
    let repeat = 100;

    let ms: Vec<f64> = vec![0.25, 0.5, 1.0, 1.5];

    println!("m,n,max,empty");
    for m in ms {
        for n in (min_n..max_n).step_by(step) {
            for _ in 0..repeat {
                let result = experiment(n, ((n as f64) * m).floor() as usize, &mut rng);
                println!("{},{},{},{}", ((n as f64) * m).floor() as usize, n, result[0], result[1]);
            }
        }
    }
}
