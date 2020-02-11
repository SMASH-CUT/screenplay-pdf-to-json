const pdf = require("pdf-parse");
import * as fs from "fs";

import { determineLines } from "./utils/determineLines";
import { parseScriptTypes } from "./utils/determineSections";
import { renderOptions } from "./config/renderOptions";
// import { determineTypes } from "./utils/determineTypes";

let dataBuffer = fs.readFileSync("../script_assets/script1.pdf");

let fooBar: any[] = [];
let debug: any[] = [];

const renderPage = async (pageData: any): Promise<string> => {
  // organize screenplay into LINES
  const parseScriptLines: any = await pageData
    .getTextContent(renderOptions)
    .then(determineLines);

  debug.push(parseScriptLines);

  const initialSectionAggregation = {
    stitchedText: [],
    previousX: -999,
    previousY: parseScriptLines[0].y,
    finalJson: []
  };

  // organize screenplay into SECTIONS
  let { finalJson } = parseScriptLines.reduce(
    parseScriptTypes,
    initialSectionAggregation
  );

  // const initialTypeAggregation = {
  //   finalParse: [],
  //   segment: {}
  // };

  // // organize screenplay into TYPES
  // const { finalParse, segment } = finalJson.reduce(
  //   determineTypes,
  //   initialTypeAggregation
  // );

  // fooBar = [...fooBar, ...finalParse, segment];
  // return JSON.stringify(finalParse, null, 4);

  fooBar = [...fooBar, ...finalJson];
  fs.appendFileSync(
    "./results/script.json",
    JSON.stringify(finalJson, null, 4)
  );
  return JSON.stringify(finalJson, null, 4);
};

let options = {
  pagerender: renderPage
};

fs.truncate("results/analyze.json", 0, function() {
  console.log("done");
  pdf(dataBuffer, options).then(() => {
    fs.writeFileSync("./results/script.json", JSON.stringify(fooBar, null, 4));
    fs.writeFileSync(
      "./results/scriptDebug.json",
      JSON.stringify(debug, null, 4)
    );
  });
});
