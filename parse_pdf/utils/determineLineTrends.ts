import { ISegment } from "./interfaces/ISegment";

const EPSILON = 3;

export const determineLineTrends = (jsonScript: ISegment[]) => {
  const lineTrends: any[] = [];
  jsonScript.forEach((segment: ISegment, mainIndex: number) => {
    if (mainIndex === 0) {
      lineTrends.push({
        line: segment.x,
        count: 1
      });
      return;
    }

    let count = 0;
    let index = 0;
    lineTrends.some((trend: any, i: number) => {
      if (Math.round(Math.abs(trend.line - segment.x)) <= EPSILON) {
        index = i;
        return;
      }
      count++;
    });

    // unique
    if (count === lineTrends.length) {
      lineTrends.push({
        text: segment.text,
        line: segment.x,
        count: 0
      });
    } else {
      lineTrends[index].count++;
    }
  });

  // console.log(lineTrends);

  return lineTrends;
};
