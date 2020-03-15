import zip from "lodash/zip";
import { gcd } from "mathjs";

interface LCGConfig {
  modulus: number;
  multiplier: number;
  increment: number;
}

function* take(n: number, list: Generator<number>) {
  yield* takeWhile(() => --n >= 0, list);
}

function* takeWhile(f: (x: number) => boolean, list: Generator<number>) {
  for (const x of list) {
    if (!f(x)) {
      break;
    }
    yield x;
  }
}

function modinv(a: number, m: number) {
  // validate inputs
  [a, m] = [Number(a), Number(m)];
  if (Number.isNaN(a) || Number.isNaN(m)) {
    return NaN; // invalid input
  }
  a = ((a % m) + m) % m;
  if (!a || m < 2) {
    return NaN; // invalid input
  }
  // find the gcd
  const s = [];
  let b = m;
  while (b) {
    [a, b] = [b, a % b];
    s.push({ a, b });
  }
  if (a !== 1) {
    throw Error(`${b} is not inversible in group modulo ${m}`);
  }
  // find the inverse
  let x = 1;
  let y = 0;
  for (let i = s.length - 2; i >= 0; --i) {
    [x, y] = [y, x - y * Math.floor(s[i].a / s[i].b)];
  }
  return ((y % m) + m) % m;
}

function crack_unknown_modulus(states: number[]): LCGConfig["modulus"] {
  console.log("Calculating missing modulus...");
  const zipped = zip(states, states.slice(1)).filter(
    ([a, b]) => a !== undefined && b !== undefined
  ) as [number, number][];
  const diffs = zipped.map(([s0, s1]) => s1 - s0);
  const zipped2 = zip(diffs, diffs.slice(1), diffs.slice(2)).filter(
    ([a, b, c]) => a !== undefined && b !== undefined && c !== undefined
  ) as [number, number, number][];
  const zeroes = zipped2.map(([t0, t1, t2]) => t2 * t0 - t1 * t1);
  const modulus = Math.abs(zeroes.reduce((acc, curr) => gcd(acc, curr)));
  return modulus;
}

function oracleUnknownMultiplier(
  states: [number, number, number],
  { modulus }: Pick<LCGConfig, "modulus">
): LCGConfig["multiplier"] {
  console.log("Calculating missing multiplier...");
  if (modulus !== undefined) {
    const multiplier =
      ((((states[2] - states[1]) * modinv(states[1] - states[0], modulus)) %
        modulus) +
        modulus) %
      modulus;
    return multiplier;
  }
  throw Error("Modulus undefined");
}

/**
 * ```
 * s1 = s0*m + c   (mod n)
 * c  = s1 - s0*m  (mod n)
 * ```
 */
function oracleUnknownIncrement(
  states: [number, number],
  { modulus, multiplier }: Omit<LCGConfig, "increment">
): LCGConfig["increment"] {
  if (multiplier !== undefined && modulus !== undefined) {
    console.log("Calculating missing increment...");
    const increment =
      (((states[1] - states[0] * multiplier) % modulus) + modulus) % modulus;
    return increment;
  }
  throw Error("Multiplier or modulus undefined");
}

function oracle(config: Partial<LCGConfig>, states: number[]): number {
  if (config.modulus === undefined && states.length >= 6) {
    config.modulus = crack_unknown_modulus(states);
  }

  if (config.multiplier === undefined && states.length >= 3) {
    config.multiplier = oracleUnknownMultiplier(
      states as [number, number, number],
      config as Pick<LCGConfig, "modulus">
    );
  }

  if (config.increment === undefined && states.length >= 2) {
    config.increment = oracleUnknownIncrement(
      states as [number, number],
      config as Omit<LCGConfig, "increment">
    );
  }

  console.log(config);
  const { modulus, multiplier, increment } = config as LCGConfig;
  const seed = states[states.length - 1];
  return (multiplier * seed + increment) % modulus;
}

function* lcg(seed: number, { modulus, multiplier, increment }: LCGConfig) {
  for (;;) {
    seed = (multiplier * seed + increment) % modulus;
    yield seed;
  }
}

const options: LCGConfig = {
  modulus: 21373737,
  multiplier: 15623,
  increment: 1836716
};

function glibc_rand() {
  return lcg(1982387123671, options);
}

const generator = glibc_rand();
const generated = Array.from(take(354, generator)).slice(344, 354);
const next = generated.pop();
const observed = generated.slice(-6);
console.log({
  options,
  observed
});
const prediction = oracle({}, observed);
console.log({ result: { next, prediction } });
console.assert(next === prediction, "Prediction is incorrect!");
