const fs = require("fs");

const file = JSON.parse(fs.readFileSync("cities.json", { encoding: "utf-8" }));

Object.values(file)
  .reduce((acc, item) => acc.concat(item.from), [])
  .filter((v, i, arr) => arr.indexOf(v) === i)
  .forEach(v => console.log(v, v, 0));

for (const entry of file) {
  console.log(Object.values(entry).join(" "));
  const tmp = entry.to;
  entry.to = entry.from;
  entry.from = tmp;
  console.log(Object.values(entry).join(" "));
}
