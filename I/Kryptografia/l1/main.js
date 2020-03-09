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

function oracle(value, { modulus, a, c }) {
  return (a * value + c) % modulus;
}

function* lcg({ modulus, a, c, seed }) {
  for (;;) {
    seed = (a * seed + c) % modulus;
    yield seed;
  }
}

const options = {
  modulus: Math.pow(2, 31),
  a: 1103515245,
  c: 12345
};

function glibc_rand() {
  return lcg({ ...options, seed: 1 });
}

const generator = glibc_rand();
const generated = Array.from(take(354, generator)).slice(344, 354);
const next = generated.pop();
const prediction = oracle(generated.pop(), options);
console.log(options);
console.log(generated);
console.log({ next, prediction });
console.assert(next === prediction, "Prediction is incorrect!");
