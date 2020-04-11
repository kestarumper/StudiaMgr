import express from "express";
import crypto from "crypto";
import bodyParser from "body-parser";
const inc = require("increment-buffer") as (buf: Buffer) => Buffer;

import { getKey } from "./store";

const app = express();
const PORT = 3000;

app.use(bodyParser.json()); // parse application/json
app.listen(PORT, function () {
  console.log("The server is running in port localhost: ", PORT);
});

let iv = Buffer.alloc(16, 0);
const algorithm = "aes-256-cbc";

async function encrypt(message: string) {
  const key = await getKey("store.jsks", "secret", "123");
  const encrypt: crypto.Cipher = crypto.createCipheriv(algorithm, key, iv);

  let encrypted = encrypt.update(message);
  encrypted = Buffer.concat([encrypted, encrypt.final()]);

  const response = {
    iv: iv.toString("hex"),
    in: message,
    out: encrypted.toString("hex"),
  };
  iv = inc(iv);

  return response;
}

app.post("/oracle", async (req, res) => {
  const { message } = req.body as { message: string };
  const response = await encrypt(message);
  res.json(response);
});

app.post("/challenge", async (req, res) => {
  const {
    messages: [m0, m1],
  } = req.body as { messages: [string, string] };
  const message = Array.from(crypto.randomBytes(1).values())[0] > 127 ? m0 : m1;
  const response = await encrypt(message);
  res.json(response);
});
