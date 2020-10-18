mod merge_sort;
mod quick_sort;

use merge_sort::mergesort;
use quick_sort::quicksort;
use rand::Rng;

use csv::Writer;
use std::error::Error;

fn write_to_csv(vec: &Vec<Experiment>, path: &str) -> Result<(), Box<Error>> {
    let mut wtr = Writer::from_path(path)?;
    for record in vec {
        wtr.serialize(record)?;
    }
    wtr.flush()?;
    Ok(())
}

pub fn make_array(capacity: usize) -> Vec<i32> {
    let mut rng = rand::thread_rng();
    return ::std::iter::repeat(())
        .map(|()| rng.gen::<i32>())
        .take(capacity)
        .collect::<Vec<i32>>();
}

fn assert_sorted(vec: &[i32]) {
    for i in 0..vec.len() - 2 {
        assert!(vec[i] <= vec[i + 1])
    }
}

type Experiment = (usize, Vec<usize>);

fn experiments(
    nmin: usize,
    nmax: usize,
    step: usize,
    repeat: usize,
    func: fn(&mut [i32]) -> usize,
) -> Vec<Experiment> {
    let mut result: Vec<Experiment> = Vec::new();
    for n in (nmin..nmax).step_by(step) {
        let compares = experiment(n, repeat, func);
        println!("n={:?}", n);
        result.push((n, compares));
    }
    return result;
}

fn experiment(n: usize, repeat: usize, func: fn(&mut [i32]) -> usize) -> Vec<usize> {
    let mut result: Vec<usize> = Vec::new();
    for i in 0..repeat {
        let arr: &mut [i32] = &mut make_array(n)[..];
        let compares = func(arr);
        assert_sorted(arr);
        result.push(compares);
    }
    return result;
}

pub fn main() {
    let nmin = 100;
    let nmax = usize::pow(10, 4) + 1;
    let step = 100;
    let repeat = 1000;
    let result = &experiments(nmin, nmax, step, repeat, quicksort);
    // let result = &experiments(nmin, nmax, step, repeat, mergesort);

    if let Err(err) = write_to_csv(&result, "experiment.csv") {
        println!("There was an error while saving to csv file");
        println!("{}", err);
        for row in result {
            println!("{:?}", row);
        }
    }
}
