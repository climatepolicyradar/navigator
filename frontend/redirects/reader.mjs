import { createReadStream } from "fs";
import readLine from "readline";
import { join } from "path";

const FALSE_VALUES = [ "0", "OFF", "NO", "FALSE"];

function toBool(value) {
  if (FALSE_VALUES.includes(value.toUpperCase())) {
    return false;
  }
  return true;
}

async function getRedirectsFromCsv(filename) {
  const redirectFile = join("redirects", filename);
  const stream = createReadStream(redirectFile);

  const lineReader = readLine.createInterface({ input: stream });
  let data = [];

  const dataReady = new Promise((resolve, reject) => {
    lineReader.on("line", (row) => {
      const rowValues = row.split(",");
      if (rowValues.length != 3) {
        reject(`ERROR: CSV file ${redirectFile} does not have 3 values on line: ${data.length+1}`)
      }
      data.push({
        source: rowValues[0],
        destination: rowValues[1],
        permanent: toBool(rowValues[2]),
      });
    });
  
    lineReader.on("close", () => {
      resolve(data);
    });

    lineReader.on("error", () => {
      reject(`ERROR: Reading redirect file named: ${redirectFile}`);
    });
  });

  return dataReady;
}

export default getRedirectsFromCsv;