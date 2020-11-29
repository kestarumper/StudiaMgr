import fs from "fs";

export type Experiment = number[];

export function createExperimentStream(fname: string, flushEvery: number) {
  const writeStream = fs.openSync(fname, "w");
  let buffer: Experiment[] = [];
  const write = (data: Experiment) => {
    buffer.push(data);
    if (buffer.length === flushEvery) {
      buffer.forEach((d) => fs.writeSync(writeStream, `${d.join(",")}\n`));
      buffer = [];
    }
  };
  const close = () => fs.closeSync(writeStream);
  return { write, close };
}

export function makeCounter() {
  let counter = 0;
  return {
    inc: () => {
      counter += 1;
    },
    get: () => counter,
  };
}
