import fs from "fs";

export type Experiment = { n: number; iterations: number };

export function createExperimentStream(fname: string, flushEvery: number) {
  const writeStream = fs.openSync(fname, "w");
  let buffer: Experiment[] = [];
  const write = (data: Experiment) => {
    buffer.push(data);
    if (buffer.length === flushEvery) {
      buffer.forEach((d) =>
        fs.writeSync(writeStream, `${d.n},${d.iterations}\n`)
      );
      buffer = [];
    }
  };
  const close = () => fs.closeSync(writeStream);
  return { write, close };
}
