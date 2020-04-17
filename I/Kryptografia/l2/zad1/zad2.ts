import axios from "axios";
import { EncryptedResponse } from "./oracle";
const inc = require("increment-buffer") as (buf: Buffer) => Buffer;

const URL = "http://localhost:3000";

const instance = axios.create({ baseURL: URL });

async function queryOracle(message: Buffer): Promise<EncryptedResponse> {
  const { data } = await instance.post("/oracle", { message });
  return data;
}

async function challenge(m0: Buffer, m1: Buffer): Promise<EncryptedResponse> {
  const { data } = await instance.post("/challenge", { messages: [m0, m1] });
  return data;
}

function xor(b1: Buffer, b2: Buffer): Buffer {
  if (b1.length != b2.length) {
    throw new Error('Lengths must be the same');
  }
  const b1vals = Array.from(b1.values());
  const b2vals = Array.from(b2.values());
  const xored = b1vals.map((v1, i) => v1 ^ b2vals[i]);
  return Buffer.from(xored);
}

console.assert(
  xor(Buffer.alloc(4, 1), Buffer.alloc(4, 0)).toString("hex") ==
    Buffer.alloc(4, 1).toString("hex"),
  "ERROR"
);

function distinguisher(c: string, c1: string) {
  if(c === c1) {
    return "m1";
  }
  return "m0";
}

(async () => {
  const m = Buffer.alloc(16, 0);
  const c = await queryOracle(m);

  const iv = Buffer.from(c.iv, 'hex');
  const iv1 = inc(Buffer.from(iv));

  const m0 = Buffer.alloc(16, 1);
  const m1 = xor(iv, iv1);

  const c1 = await challenge(m0, m1);

  console.log({ c, m0, m1, iv, iv1, c1 });
  console.log(`Challenge encrypted message: ${distinguisher(c.out, c1.out)}`);
})();
