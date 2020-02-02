const pdf = require("pdf-parse");
import * as fs from "fs";

import { renderText } from "./utils/renderText";

let dataBuffer = fs.readFileSync("../script_assets/script.pdf");

const finalJson: any = [];

// default render callback
const renderPage = async (pageData: any): Promise<string> => {
  //check documents https://mozilla.github.io/pdf.js/
  let render_options = {
    //replaces all occurrences of whitespace with standard spaces (0x20). The default value is `false`.
    normalizeWhitespace: true,
    //do not attempt to combine same line TextItem's. The default value is `false`.
    disableCombineTextItems: false
  };

  const renderResult: any = await pageData
    .getTextContent(render_options)
    .then(renderText);

  // console.log(JSON.stringify(renderResult, null, 4));

  renderResult.parsedScript.forEach((textObj: any) => {
    if (Object.keys(textObj).length && textObj.text.trim() !== "") {
      finalJson.push(JSON.stringify(textObj, null, 4));
    }
  });

  return JSON.stringify(renderResult, null, 4);
};

let options = {
  pagerender: renderPage
};

pdf(dataBuffer, options).then(() => {
  fs.writeFileSync("./results/script.json", [finalJson]);
});
