const pdf = require("pdf-parse");
import * as fs from "fs";

import { determineLines } from "./utils/renderText";
import { parseScriptTypes } from "./utils/parseType";
import { renderOptions } from "./config/renderOptions";

let dataBuffer = fs.readFileSync("../script_assets/script.pdf");

let fooBar: any[] = [];

const renderPage = async (pageData: any): Promise<string> => {
  // organize screenplay text into individual LINES
  const parseScriptLines: any = await pageData
    .getTextContent(renderOptions)
    .then(determineLines);

  const initialAggregate = {
    stichedText: "",
    previousX: -999,
    previousY: parseScriptLines[0].y,
    finalJson: []
  };

  // organize screenplay text into individual TYPES
  const { finalJson } = parseScriptLines.reduce(
    parseScriptTypes,
    initialAggregate
  );

  fooBar.push(finalJson);
  return JSON.stringify(finalJson, null, 4);
};

let options = {
  pagerender: renderPage
};

fs.truncate("results/analyze.json", 0, function() {
  console.log("done");
  pdf(dataBuffer, options).then(() => {
    fs.writeFileSync("./results/script.json", JSON.stringify(fooBar, null, 4));
  });
});
