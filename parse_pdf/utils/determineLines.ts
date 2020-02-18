import { PDFExtract, PDFExtractOptions } from "pdf.js-extract";

import { IFinalParse, ILineParse } from "../utils/interfaces/IFinalParse";

const pdfExtract = new PDFExtract();
const options: PDFExtractOptions = {
  normalizeWhitespace: true,
  disableCombineTextItems: false,
  verbosity: 1
};

export const determineLines = async (filePath: string) => {
  const data = await pdfExtract.extract(filePath, options);

  const finalParse: IFinalParse[] = [];

  try {
    let text = "";
    let previousY = data.pages[0].content[0].y;
    let previousX = -999;
    let page = 0;

    data.pages.forEach(currPage => {
      page = currPage.pageInfo.num;
      const lineParse: ILineParse[] = [];
      currPage.content.forEach(({ x, y, str, height, width }: any) => {
        if (y === previousY) {
          text += str;
        } else {
          lineParse.push({
            text,
            x: previousX,
            y: previousY,
            height,
            width
          });
          text = str;
          previousX = x;
          previousY = y;
        }
      });
      finalParse.push({
        page,
        content: lineParse
      });
    });
  } catch (error) {
    console.log(error);
  }
  return finalParse;
};
