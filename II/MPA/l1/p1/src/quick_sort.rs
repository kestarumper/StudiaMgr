use std::cmp;

pub fn quicksort(vec: &mut [i32]) {
    let len: usize = vec.len();
    if len <= 1 {
        return;
    }

    let pivot: usize = 0;
    vec.swap(pivot, len / 2);

    let mut left: usize = 1;
    let mut right: usize = vec.len() - 1;

    loop {
        while left < len && &vec[left] < &vec[pivot] {
            left += 1
        }
        while right > 0 && &vec[right] > &vec[pivot] {
            right -= 1
        }
        if left >= right {
            break;
        }
        vec.swap(left, right);
        left += 1;
        right -= 1;
    }

    vec.swap(pivot, right);

    quicksort(&mut vec[0..cmp::min(left - 1, right)]);
    quicksort(&mut vec[cmp::max(left, right + 1)..]);
}

#[cfg(test)]
mod tests {
    use super::quicksort;
    use rand::Rng;


    #[test]
    fn test_random() {
        let mut rng = rand::thread_rng();

        for _ in 0u64..10_000u64 {
            let len: usize = rng.gen::<usize>();
            let mut vector = ::std::iter::repeat(())
                .map(|()| rng.gen::<i32>())
                .take((len % 64) + 1)
                .collect::<Vec<i32>>();

            quicksort(&mut vector);

            for i in 0..vector.len() - 1 {
                assert!(vector[i] <= vector[i + 1])
            }
        }
    }
}
