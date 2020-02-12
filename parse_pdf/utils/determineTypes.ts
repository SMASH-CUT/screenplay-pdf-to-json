import { headingEnum } from "../enums/headingEnum";
import { timeEnum } from "../enums/timeEnum";

interface IParseScriptTypes {
  finalParse: any[];
  segment: any;
}

interface ITextObj {
  text: string[];
}

const determineHeading = ({ text: textArr }: ITextObj) => {
  return Object.values(headingEnum).some((transition: any) => {
    return textArr[0].includes(transition);
  });
};

const determineDay = (text: string) => {
  return Object.values(timeEnum).some((transition: any) => {
    return text.includes(transition);
  });
};

const extractHeading = ({ text }: ITextObj): any => {
  let curr = text[0].split(".");
  let location: any = [];
  let time = "";

  const region = curr[0];
  if (curr.length > 1) {
    curr = curr[1].split("-");
    location = curr;
    if (determineDay(curr[curr.length - 1])) {
      console.log(curr);
      time = curr[curr.length - 1];
    }
  }

  return { region, location, time };
};

export const determineTypes = (
  { finalParse, segment }: IParseScriptTypes,
  currentTextObj: any
) => {
  if (determineHeading(currentTextObj)) {
    // if new heading, then push the current segment to finalParse
    finalParse.push(segment);
    segment = {};

    const { region, location, time } = extractHeading(currentTextObj);
    segment = {
      region,
      location,
      time,
      nest: []
    };
  } else {
    segment.nest.push(currentTextObj.text);
  }

  return { finalParse, segment };
};
