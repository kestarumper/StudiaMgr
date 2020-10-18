mod merge_sort;
mod quick_sort;

use merge_sort::mergesort;
use quick_sort::quicksort;
use rand::Rng;

pub fn make_array(capacity: usize, min: i32, max: i32) -> Vec<i32> {
    let mut rng = rand::thread_rng();
    return ::std::iter::repeat(())
        .map(|()| rng.gen::<i32>())
        .map(|num| (num % max + min) % max)
        .take(capacity)
        .collect::<Vec<i32>>();
}

fn assert_sorted(vec: &[i32]) {
    for i in 0..vec.len() - 2 {
        assert!(vec[i] <= vec[i + 1])
    }
}

pub fn main() {
    let arr: &mut [i32] = &mut make_array(usize::pow(10, 1), -1000, 1000)[..];
    let qc_compares = quicksort(arr);

    assert_sorted(arr);

    println!("Total QS compares: {}", qc_compares);

    let arr2: &mut [i32] = &mut make_array(usize::pow(10, 1), -1000, 1000)[..];
    let ms_compares = mergesort(arr2);

    assert_sorted(arr2);

    println!("Total MS compares: {}", ms_compares);
}
