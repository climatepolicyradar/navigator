import { createReadStream } from "fs";
import readLine from "readline";
import { join } from "path";

const FALSE_VALUES = ["0", "OFF", "NO", "FALSE"];


/**
 * read - Reads redirect definitions given the filename - currently only CSV.
 *
 * @param {*} filename - Only the filename which should be a file in the top-level "redirects" folder
 * @returns Promise to an array of redirects
 */
const read = (filename) => {

  /**
   * readFromCSV - Reads redirects from file - for use by a Promise.
   *
   * @param {*} redirectFile - file to read from.
   * @param {*} resolve - calls the function to return the array of redirects.
   * @param {*} reject - calls this function when an error occurs with a string represtation of the error.
   */
  function readFromCSV(redirectFile, resolve, reject) {

    // toBool - returns a boolean given a string
    const toBool = (value) => !(FALSE_VALUES.includes(value.toUpperCase()));

    const stream = createReadStream(redirectFile);
    const lineReader = readLine.createInterface({ input: stream });
    let data = [];

    lineReader.on("line", (row) => {
      const rowValues = row.split(",");
      if (rowValues.length != 3) {
        reject(`ERROR: CSV file ${redirectFile} does not have 3 values on line: ${data.length + 1}`)
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
  }

  return new Promise((resolve, reject) => readFromCSV(join("redirects", filename), resolve, reject));
}


export default read;