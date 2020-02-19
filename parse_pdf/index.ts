import * as fs from "fs";
import * as util from "util";
import * as shell from "shelljs";

import { sortDualDialogue } from "./utils/sortDualDialogue";
// import { IFinalParse } from "./utils/interfaces/IFinalParse";

const readFile = fileName => util.promisify(fs.readFile)(fileName, "utf8");

shell.chmod(777, "./utils/newDetermineLines.py");
shell.exec("echo Y > pipenv --python 3");
shell.exec("pipenv install pdfminer");
shell.exec("pipenv shell");
shell.exec("python3 ./utils/newDetermineLines.py");
console.log("here after async call");

(async () => {
  const rawParse = await readFile("./result.json");
  let finalParse: any = JSON.parse(rawParse).pdf;
  finalParse = sortDualDialogue(finalParse);
  fs.writeFileSync("./finalResults.json", JSON.stringify(finalParse, null, 4));
})();
