import { headingEnum } from "../enums/headingEnum";

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

// const determineSceneDirection = (textObj: ITextObj) => {
//   return true;
// };
// const determineDialogue = (textObj: ITextObj) => {
//   return true;
// };
// const determineTransition = (textObj: ITextObj) => {
//   return true;
// };

const extractHeading = ({ text }: ITextObj): any => {
  let curr = text[0].split(".");
  const region = curr[0];
  curr = curr[1].split("-");
  const location = curr.slice(0, -1);
  const time = curr[curr.length - 1];

  return { region, location, time };
};

// const extractSceneDirection = (textObj: ITextObj): any => {
//   return true;
// };

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
