mod merge_sort;
mod quick_sort;

use merge_sort::mergesort;
use quick_sort::quicksort;
use rand::Rng;

pub fn make_array(capacity: usize) -> Vec<i32> {
    let mut rng = rand::thread_rng();
    let len: usize = rng.gen::<usize>();
    return ::std::iter::repeat(())
        .map(|()| rng.gen::<i32>())
        .take(capacity)
        .collect::<Vec<i32>>();
}

// pub fn main() {
//     let arr: &mut [i32] = &mut make_array(usize::pow(10, 6))[..];
//     mergesort(arr);
//     println!("{:?}", arr);
// }

pub fn main() {
    let arr: &mut [i32] = &mut make_array(usize::pow(10, 1))[..];
    quicksort(arr);
    println!("{:?}", arr);

    for i in 0..arr.len() - 2 {
        assert!(arr[i] <= arr[i + 1])
    }
}
