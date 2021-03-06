fn merge(arr1: &[i32], arr2: &[i32], ret: &mut [i32]) -> usize {
    let mut compares: usize = 0;
    let mut left = 0; // Head of left pile.
    let mut right = 0; // Head of right pile.
    let mut index = 0;

    // Compare element and insert back to result array.
    while left < arr1.len() && right < arr2.len() {
        compares += 1;
        if arr1[left] <= arr2[right] {
            ret[index] = arr1[left];
            left += 1;
        } else {
            ret[index] = arr2[right];
            right += 1;
        }
        index += 1;
    }

    // Copy the elements to returned array.
    if left < arr1.len() {
        ret[index..].copy_from_slice(&arr1[left..]);
    }
    if right < arr2.len() {
        ret[index..].copy_from_slice(&arr2[right..]);
    }

    return compares;
}

pub fn mergesort(arr: &mut [i32]) -> usize {
    let mut compares: usize = 0;

    let mid = arr.len() / 2;
    if mid == 0 {
        return compares;
    }

    compares += mergesort(&mut arr[..mid]);
    compares += mergesort(&mut arr[mid..]);

    // Create an array to store intermediate result.
    let mut ret = arr.to_vec();

    // Merge the two piles.
    compares += merge(&arr[..mid], &arr[mid..], &mut ret[..]);

    // Copy back the result back to original array.
    arr.copy_from_slice(&ret);

    return compares;
}

#[cfg(test)]
mod tests {
    use super::mergesort;
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

            mergesort(&mut vector);

            for i in 0..vector.len() - 1 {
                assert!(vector[i] <= vector[i + 1])
            }
        }
    }
}
