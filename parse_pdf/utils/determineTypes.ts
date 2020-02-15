import { headingEnum } from "../enums/headingEnum";
import { timeEnum } from "../enums/timeEnum";
import { ISegment } from "./interfaces/ISegment";
import { characterNameEnum } from "../enums/characterNameEnum";

interface INest {
  region: string;
  location: string;
  time: string;
  nest: any[];
}

const determineHeading = ({ text: textArr }: ISegment) => {
  return Object.values(headingEnum).some((transition: any) => {
    return textArr[0].includes(transition);
  });
};

const determineDay = (text: string) => {
  return Object.values(timeEnum).some((transition: any) => {
    return text.includes(transition);
  });
};

const determineCharacter = ({ text: textArr }: ISegment) => {
  if (textArr.length > 1) {
    return false;
  }
  let character = textArr[0].split(" ");
  if (character[0] !== character[0].toUpperCase()) {
    return false;
  }
  if (character.length === 1) {
    if (character[0].includes(".")) {
      return false;
    }
    return true;
  }

  return Object.values(characterNameEnum).some((modifier: any) => {
    return character[1].includes(modifier);
  });
};

const extractCharacter = (
  { text: textArr }: ISegment,
  { text: dialogue }: ISegment,
  { text: parenthetical }: ISegment
) => {
  const split = textArr[0].split(" ");
  return {
    character: split[0],
    modifier: split.length > 1 ? split[1] : "",
    parenthetical: parenthetical ? parenthetical[0] : "",
    dialogue
  };
};

const extractHeading = ({ text }: ISegment, lineTrends: any): any => {
  let curr = lineTrends;
  curr = text[0].split(".");
  let location: any = [];
  let time = "";

  const region = curr[0];

  if (curr.length > 1) {
    let divider = ".";
    const dayOrNot = determineDay(curr[curr.length - 1]);
    location = dayOrNot ? curr.slice(1, -1) : curr;

    if (curr.length === 2) {
      divider = ",";
      const some = curr.some((el: string) => el.includes("-"));
      if (some) {
        divider = "-";
      }
      curr = curr[1].split(divider);
      location = dayOrNot ? curr.slice(0, -1) : curr;
    }
    time = dayOrNot ? curr[curr.length - 1] : "";
  }

  return { region, location, time };
};

export const determineTypes = (lineTrends: any, scriptSections: ISegment[]) => {
  let finalParse = [];
  let segment: INest = {
    region: "",
    location: "",
    time: "",
    nest: []
  };

  for (let index = 0; index < scriptSections.length; index++) {
    const currentTextObj = scriptSections[index];

    if (determineHeading(currentTextObj)) {
      // if new heading, then push the current segment to finalParse
      finalParse.push(segment);
      const { region, location, time } = extractHeading(
        currentTextObj,
        lineTrends
      );
      segment = {
        region,
        location,
        time,
        nest: []
      };
    } else if (determineCharacter(currentTextObj)) {
      index++;
      const containsParentheticals =
        scriptSections[index].text.length === 1 &&
        scriptSections[index].text[0].includes("(");
      if (containsParentheticals) {
        segment.nest.push(
          extractCharacter(
            currentTextObj,
            scriptSections[index + 1],
            scriptSections[index]
          )
        );
        index++;
      } else {
        segment.nest.push(
          extractCharacter(currentTextObj, scriptSections[index], {
            text: [""],
            x: 0,
            y: 0
          })
        );
      }
    } else {
      segment.nest.push(currentTextObj.text);
    }
  }

  finalParse.push(segment);

  return finalParse;
};
