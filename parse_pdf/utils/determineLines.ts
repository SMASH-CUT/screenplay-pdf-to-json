import { PDFExtract, PDFExtractOptions } from "pdf.js-extract";

import { IFinalParse } from "../utils/interfaces/IFinalParse";

const pdfExtract = new PDFExtract();
const options: PDFExtractOptions = {
  normalizeWhitespace: false,
  disableCombineTextItems: false
};

export const determineLines = async (filePath: string) => {
  const data = await pdfExtract.extract(filePath, options);

  const finalParse: IFinalParse[] = [];
  try {
    let text = "";
    let previousY = data.pages[0].content[0].y;
    let previousX = -999;

    data.pages.forEach(page => {
      page.content.forEach(({ x, y, str, height, width }: any) => {
        if (y === previousY) {
          text += str;
        } else {
          finalParse.push({ text, x: previousX, y: previousY, height, width });
          text = str;
          previousX = x;
          previousY = y;
        }
      });
    });
  } catch (error) {
    console.log(error);
  }
  return finalParse;
};
