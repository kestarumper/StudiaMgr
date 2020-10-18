fn partition(vec: &mut [i32], lo: i32, hi: i32) -> (i32, usize) {
    let mut compares: usize = 0;
    let pivot = vec[((lo + hi) / 2) as usize];
    let mut i: i32 = lo - 1;
    let mut j: i32 = hi + 1;
    loop {
        loop {
            i += 1;
            compares += 1;
            if vec[i as usize] >= pivot {
                break;
            }
        }
        loop {
            j -= 1;
            compares += 1;
            if vec[j as usize] <= pivot {
                break;
            }
        }

        compares += 1;
        if i >= j {
            return (j, compares);
        }
        vec.swap(i as usize, j as usize);
    }
}

fn quicksort_helper(vec: &mut [i32], lo: i32, hi: i32) -> usize {
    if lo < hi {
        let (p, compares) = partition(vec, lo, hi);
        let c1 = quicksort_helper(vec, lo, p);
        let c2 = quicksort_helper(vec, p + 1, hi);
        return compares + c1 + c2;
    }
    return 0;
}

pub fn quicksort(vec: &mut [i32]) -> usize {
    return quicksort_helper(vec, 0, (vec.len() - 1) as i32);
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
