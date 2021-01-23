/**
 * Shuffles array in place. ES6 version
 * @param {Array} a items An array containing the items.
 */
function shuffle(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

const LEFT_BRACKET = 1;
const RIGHT_BRACKET = -1;

/**
 * Generates random balanced sequence
 * http://www.cs.otago.ac.nz/staffpriv/mike/Papers/RandomGeneration/RandomBinaryTrees.pdf
 * https://gist.github.com/rygorous/d57941fa5ae6beb59f17bc30793d3d75
 * @param {number} n
 * @returns {number[]}
 */
function randomBalancedSequence(n) {
  // Generate a randomly shuffled sequence of n +1s and n -1s
  // These are steps 1 and 2 of the algorithm in the pape
  const seq = shuffle(
    Array.from({ length: n }, () => 1).concat(
      Array.from({ length: n }, () => -1)
    )
  );

  // This now corresponds to a balanced bracket sequence (same number of
  // opening and closing brackets), but it might not be well-formed
  // (brackets closed before they open). Fix this up using the bijective
  // map in the paper (step 3).
  const prefix = [];
  let suffix = [];
  let word = [];
  let partial_sum = 0;
  for (const s of seq) {
    word.push(s);
    partial_sum += s;
    if (partial_sum == 0) {
      // at the end of an irreducible balanced word
      if (s === -1) {
        // it was well-formed! append it.
        prefix.push(...word);
      } else {
        // it was not well-formed! fix it.
        prefix.push(1);
        suffix = [-1, ...word.slice(1, -1).map((v) => -v), ...suffix];
      }
      word = [];
    }
  }

  return prefix.concat(suffix);
}

function validate(input) {
  let tmp = 0;
  for (let c of input) {
    if (c === LEFT_BRACKET) tmp++;
    else if (c === RIGHT_BRACKET && --tmp < 0)
      throw new Error("Unexpected ')'"); // Unexpected  ')'
  }
  return tmp === 0; // False if unbalanced
}

function makeBinaryTree(input) {
  let i = 0; // character index in input
  let min = Number.POSITIVE_INFINITY;
  let max = Number.NEGATIVE_INFINITY;
  recur(0);

  return [min, max];

  function recur(level) {
    if (i >= input.length || input[i++] === RIGHT_BRACKET) {
      return null;
    }
    const node = { left: recur(level + 1), right: null };
    if (i >= input.length || input[i] === RIGHT_BRACKET) {
      if (node.left === null && node.right === null) {
        min = Math.min(min, level);
        max = Math.max(max, level);
      }
      i++;
      return node;
    }
    node.right = recur(level + 1);
    return node;
  }
}

function experiment(n, repeat) {
  Array.from({ length: repeat }, () => randomBalancedSequence(n))
    .map(makeBinaryTree)
    .forEach(([min, max]) => console.log(`${n},${min},${max}`));
}

const n_start = 1000;
const n_end = 50000;
const n_step = n_start;
const repeat = 100;
console.log("n,min,max");
for (let n = n_start; n <= n_end; n += n_step) {
  experiment(n, repeat);
}
