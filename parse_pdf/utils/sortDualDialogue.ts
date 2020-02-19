import { IFinalParse, ILineParse } from "../utils/interfaces/IFinalParse";

const initSort = (finalParse: IFinalParse[]) => {
  const sortedFinalParse: any[] = [];
  for (let pageIndex = 0; pageIndex < finalParse.length; pageIndex++) {
    const page: ILineParse[] = finalParse[pageIndex].content;
    sortedFinalParse.push({
      page: finalParse[pageIndex].page,
      content: []
    });
    for (let lineIndex = 0; lineIndex < page.length - 1; lineIndex++) {
      let line: ILineParse = page[lineIndex];
      let nextLine: ILineParse = page[lineIndex + 1];
      const latestFinalIndex = sortedFinalParse.length - 1;
      if (line.y === nextLine.y) {
        sortedFinalParse[latestFinalIndex].content.push([line, nextLine]);
        lineIndex++;
      } else {
        sortedFinalParse[latestFinalIndex].content.push(line);
      }
    }
  }
  return sortedFinalParse;
};
export const sortDualDialogue = (finalParse: IFinalParse[]) => {
  const sortedFinalParse: any[] = initSort(finalParse);
  return sortedFinalParse;
  const dualDialogueFinal: any = [];
  for (let i = 0; i < sortedFinalParse.length; i++) {
    const pageInfo = sortedFinalParse[i];
    dualDialogueFinal.push({ page: pageInfo.page });
    for (let j = 0; j < sortedFinalParse[i].content.length; j++) {
      if (Array.isArray(pageInfo.content[j])) {
        while (Array.isArray(pageInfo.content[j])) {
          let left = pageInfo.content[j][0];
          let right = pageInfo.content[j][1];
          console.log(`${left.text}, ${right.text}`);
          if (left.x > right.x) {
            const swap = left;
            left = right;
            right = swap;
          }
          if (
            left.text === left.text.toUpperCase() &&
            right.text === right.text.toUpperCase()
          ) {
            dualDialogueFinal[dualDialogueFinal.length - 1] = [
              { character: left.text, dialogue: [] },
              { character: right.text, dialogue: [] }
            ];
          } else {
            dualDialogueFinal[dualDialogueFinal.length - 1][0].dialogue.push(
              left.text
            );
            dualDialogueFinal[dualDialogueFinal.length - 1][1].dialogue.push(
              right.text
            );
          }
          j++;
        }
        j--;
      } else {
        dualDialogueFinal.push(pageInfo.content[j]);
      }
    }
  }
  return dualDialogueFinal;
};
