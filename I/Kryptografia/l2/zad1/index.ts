import * as crypto from "crypto";
import * as fs from "fs";
import * as zlib from "zlib";
import * as yargs from "yargs";
import * as tmp from "tmp";

const argv = yargs.options({
  dec: { type: "boolean" },
  mode: { type: "string", demandOption: true, choices: ["OFB", "CTR", "CBC"] },
  file: { type: "string", demandOption: true },
  key: { type: "string", demandOption: true },
}).argv;

const algorithm = `aes-256-${argv.mode.toLowerCase()}`;
const key = Buffer.alloc(32, 1);
const iv = Buffer.alloc(16, 0);

function encryptFile(fin: fs.ReadStream, fout: fs.WriteStream) {
  const zip = zlib.createGzip();
  const encrypt = crypto.createCipheriv(algorithm, key, iv);
  return fin.pipe(zip).pipe(encrypt).pipe(fout);
}

function decryptFile(fin: fs.ReadStream, fout: fs.WriteStream) {
  const decrypt = crypto.createDecipheriv(algorithm, key, iv);
  const unzip = zlib.createGunzip();
  return fin.pipe(decrypt).pipe(unzip).pipe(fout);
}

const tmpFile = tmp.fileSync();
try {
  const r = fs.createReadStream(argv.file);
  const w = fs.createWriteStream(tmpFile.name);

  if (argv.dec) {
    console.log("DEC")
    decryptFile(r, w);
  } else {
    console.log("ENC")
    encryptFile(r, w);
  }

  fs.unlinkSync(argv.file);
  fs.renameSync(tmpFile.name, argv.file);
} catch (error) {
  tmpFile.removeCallback();
  console.log(error);
}
