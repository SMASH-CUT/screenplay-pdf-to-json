import { IFinalParse } from "./interfaces/IFinalParse";

export const sortLine = (finalParse: IFinalParse[]) => {
  const sortFix: IFinalParse[] = [];
  finalParse.forEach((sec: IFinalParse) => {
    sortFix.push({
      page: sec.page,
      content: sec.content.sort((a, b) => {
        return a.y - b.y;
      })
    });
  });
  return sortFix;
};
