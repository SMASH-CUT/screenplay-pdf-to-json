import { transitionsEnum } from "../enums/transitionsEnum";
import { IFinalParse } from "../utils/interfaces/IFinalParse";

const checkTransition = (text: string) => {
  return Object.values(transitionsEnum).some((transition: any) => {
    return text.includes(transition);
  });
};

const checkSlugline = (text: string) => {
  return text.includes("EXT.") || text.includes("INT.");
};

const cleanScript = (text: string) => {
  return !(text.includes("CONTINUED:") || text.trim() === "");
};

const parseType = (
  finalJson: any,
  currentTextObj: any,
  stitchedText: string[],
  previousX: number,
  previousY: number
) => {
  const { x, y, height, width } = currentTextObj;
  let { text } = currentTextObj;

  if (
    !currentTextObj.hasOwnProperty("text") ||
    currentTextObj.text.trim() === ""
  ) {
    return { finalJson, stitchedText, previousX, previousY };
  }

  // if width different
  if (Math.round(Math.abs(previousX - x)) > 0) {
    // and y different, than different section
    if (previousY != y) {
      if (stitchedText.length) {
        finalJson.push({
          text: stitchedText,
          x: previousX,
          y: previousY,
          height,
          width
        });
      }

      previousX = x;
      previousY = y;
      stitchedText = [];

      if (checkSlugline(text) || checkTransition(text)) {
        finalJson.push({ text: [text.trim()], x, y, height, width });
        stitchedText = [];
      } else if (cleanScript(text)) {
        stitchedText = [text.trim()];
      }
    }

    // and y same, than same section
    else {
      previousX = Math.min(x, previousX);
      if (cleanScript(text)) {
        stitchedText.push(text.trim());
      }
    }
  }
  // different line
  else if (previousY != y) {
    // if heading/transition, push current stitch and push heading/transition immediately
    if (checkSlugline(text) || checkTransition(text)) {
      if (stitchedText.length) {
        finalJson.push({
          text: stitchedText,
          x: previousX,
          y: previousY,
          height,
          width
        });
      }
      if (cleanScript(text)) {
        finalJson.push({ text: [text.trim()], x, y, height, width });
      }
      stitchedText = [];
    } else {
      if (cleanScript(text)) {
        const lastSentence =
          stitchedText.length > 0 ? stitchedText[stitchedText.length - 1] : "";
        if (
          lastSentence.length > 0 &&
          !(checkSlugline(lastSentence) && checkTransition(lastSentence)) &&
          lastSentence.charAt(lastSentence.length - 1) != "." &&
          lastSentence.charAt(lastSentence.length - 1) != ")" &&
          lastSentence.charAt(lastSentence.length - 1) != "-"
        ) {
          stitchedText[stitchedText.length - 1] += text.trim();
        } else {
          stitchedText.push(text.trim());
        }
      }
    }
    previousY = y;
  }

  return { finalJson, stitchedText, previousX, previousY };
};

export const determineSections = (finalParse: IFinalParse[]) => {
  let stitchedText: string[] = [];
  let previousX = -999;
  let previousY = finalParse[0].y;
  let finalJson: IFinalParse[] = [];

  for (let index = 0; index < finalParse.length; index++) {
    const currentTextObj = finalParse[index];
    ({ finalJson, stitchedText, previousX, previousY } = parseType(
      finalJson,
      currentTextObj,
      stitchedText,
      previousX,
      previousY
    ));
  }

  return finalJson;
};
