import crypto from "crypto";
import fs from "fs";
import zlib from "zlib";
import yargs from "yargs";
import tmp from "tmp";

import { getKey } from "./store";

const argv = yargs.options({
  dec: { type: "boolean" },
  mode: { type: "string", demandOption: true, choices: ["OFB", "CTR", "CBC"] },
  file: { type: "string", demandOption: true },
  storeFile: { type: "string", demandOption: true },
  password: { type: "string", demandOption: true },
  key: { type: "string", demandOption: true },
}).argv;

const algorithm = `aes-256-${argv.mode.toLowerCase()}`;
const iv = Buffer.alloc(16, 0);

async function encryptFile(key: Buffer, fin: fs.ReadStream, fout: fs.WriteStream) {
  const zip = zlib.createGzip();
  const encrypt = crypto.createCipheriv(algorithm, key, iv);
  return fin.pipe(zip).pipe(encrypt).pipe(fout);
}

async function decryptFile(key: Buffer, fin: fs.ReadStream, fout: fs.WriteStream) {
  const decrypt = crypto.createDecipheriv(algorithm, key, iv);
  const unzip = zlib.createGunzip();
  return fin.pipe(decrypt).pipe(unzip).pipe(fout);
}

(async () => {
  const tmpFile = tmp.fileSync();
  try {
    const r = fs.createReadStream(argv.file);
    const w = fs.createWriteStream(tmpFile.name);
    const key = await getKey(argv.storeFile, argv.key, argv.password);

    if (argv.dec) {
      await decryptFile(key, r, w);
    } else {
      await encryptFile(key, r, w);
    }
    console.log(iv.toString('hex'))

    fs.renameSync(tmpFile.name, argv.file);
  } catch (error) {
    tmpFile.removeCallback();
    console.log(error);
  }
})().catch(console.error);
