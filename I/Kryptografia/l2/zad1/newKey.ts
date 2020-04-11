import yargs from "yargs";

import { newKey } from "./store";

const argv = yargs.options({
  storeFile: { type: "string", demandOption: true },
  password: { type: "string", demandOption: true },
  key: { type: "string", demandOption: true },
}).argv;

newKey(argv.storeFile, argv.key, argv.password)
  .then(console.log)
  .catch(console.error);
