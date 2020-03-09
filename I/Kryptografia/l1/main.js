function* lcg(modulus, a, c, seed) {
  for (;;) {
    seed = (a * seed + c) % modulus;
    yield seed;
  }
}

function glibc_rand() {
  return lcg(Math.pow(2, 31), 1103515245, 12345, 1);
}

// list containing at most first n elements
function* take(n, list) {
  yield* takeWhile(() => --n >= 0, list);
}

function* takeWhile(f, list) {
  for (var x of list) {
    if (!f(x)) {
      break;
    }
    yield x;
  }
}

const generator = glibc_rand();
console.log(Array.from(take(354, generator)).slice(344, 354));
