import crypto from "crypto";
import fs from "fs";
import util from "util";
import { createStore } from "key-store";

const readFile = util.promisify(fs.readFile);
const writeFile = util.promisify(fs.writeFile);

export async function createFileStore(filePath: string) {
  const saveKeys = (data: object) =>
    writeFile(filePath, JSON.stringify(data, null, 2), "utf8");
  const readKeys = async () => JSON.parse(await readFile(filePath, "utf8"));

  return createStore<string>(saveKeys, await readKeys());
}

export async function getKey(filePath: string, id: string, password: string) {
  const keyStore = await createFileStore(filePath);
  return Buffer.from(keyStore.getPrivateKeyData(id, password), "hex");
}

export async function newKey(
  filePath: string,
  id: string,
  password: string,
  keyLength: number = 32
) {
  const keyStore = await createFileStore(filePath);
  return (
    keyStore.saveKey(
      id,
      password,
      crypto.randomBytes(keyLength).toString("hex")
    ) && id
  );
}
