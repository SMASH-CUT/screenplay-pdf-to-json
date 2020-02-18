// const pdf = require("pdf-parse");
// import { PDFExtract, PDFExtractOptions } from "pdf.js-extract";
import * as fs from "fs";

import { determineLines } from "./utils/determineLines";
// import { sortLine } from "./utils/sortLine";
// import { determineSections } from "./utils/determineSections";
// import { renderOptions } from "./config/renderOptions";
// import { determineTypes } from "./utils/determineTypes";
// import { determineLineTrends } from "./utils/determineLineTrends";

// let dataBuffer = fs.readFileSync("../script_assets/spiderverse.pdf");

// let scriptSections: any[] = [];
// let lastSection = {
//   text: "",
//   x: 0,
//   y: 0
// };
// let debug: any[] = [];

// const renderPage = async (pageData: any): Promise<string> => {
//   // organize screenplay into LINES
//   const parseScriptLines: any = await pageData
//     .getTextContent(renderOptions)
//     .then(determineLines);

//   debug.push(parseScriptLines);

//   const initialSectionAggregation = {
//     stitchedText: [],
//     previousX: -999,
//     previousY: parseScriptLines[0].y,
//     finalJson: []
//   };

//   // organize screenplay into SECTIONS
//   let {
//     finalJson,
//     stitchedText,
//     previousX,
//     previousY
//   } = parseScriptLines.reduce(determineSections, initialSectionAggregation);
//   lastSection = {
//     text: stitchedText,
//     x: previousX,
//     y: previousY
//   };
//   scriptSections = [...scriptSections, ...finalJson];
//   return JSON.stringify(finalJson, null, 4);
// };

// let optionsz = {
//   pagerender: renderPage
// };

// pdf(dataBuffer, optionsz).then(() => {
//   scriptSections = [...scriptSections, lastSection];
//   const lineTrends = determineLineTrends(scriptSections);

//   // organize screenplay into TYPES
//   scriptSections = determineTypes(lineTrends, scriptSections);
//   fs.writeFileSync(
//     "./results/script.json",
//     JSON.stringify(scriptSections, null, 4)
//   );
//   fs.writeFileSync(
//     "./results/scriptDebug.json",
//     JSON.stringify(debug, null, 4)
//   );
// });

(async () => {
  const filePath = "../script_assets/spiderverse.pdf";
  let finalParse = await determineLines(filePath);
  // finalParse = sortLine(finalParse);

  // organize screenplay into SECTIONS
  // finalParse = determineSections(finalParse);
  // let lastSection = {
  //   text: stitchedText,
  //   x: previousX,
  //   y: previousY
  // };
  // scriptSections = [...scriptSections, ...finalJson];
  fs.writeFileSync(
    "./results/newScript.json",
    JSON.stringify(finalParse, null, 4)
  );
})();
