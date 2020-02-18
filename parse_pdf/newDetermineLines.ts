import PDFParser from "pdf2json";
import * as fs from "fs";

let pdfParser = new PDFParser();

pdfParser.on("pdfParser_dataError", errData =>
  console.error(errData.parserError)
);
pdfParser.on("pdfParser_dataReady", pdfData => {
  fs.writeFileSync("./script.json", JSON.stringify(pdfData, null, 4));
  const finalParse: any = [];

  try {
    let previousY = -999;
    let previousX = -999;
    let page = 1;

    pdfData.formImage.Pages.forEach(currPage => {
      let text: any = "";
      const lineParse: any = [];
      currPage.Texts.forEach(({ x, y, R }: any) => {
        if (y === previousY) {
          text += R[0].T;
        } else {
          lineParse.push({
            text,
            x: previousX,
            y: previousY
          });
          text = R[0].T;
          previousX = x;
          previousY = y;
        }
      });
      finalParse.push({
        page,
        content: lineParse
      });
      page++;
    });
  } catch (error) {
    console.log(error);
  }

  fs.writeFileSync("newScript.json", JSON.stringify(finalParse, null, 4));
});

pdfParser.loadPDF("../script_assets/spiderverse.pdf");
