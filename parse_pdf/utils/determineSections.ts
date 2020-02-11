import { transitionsEnum } from "../enums/transitionsEnum";

interface IParseScriptTypes {
  finalJson: any[];
  stitchedText: string[];
  previousX: number;
  previousY: number;
}

const checkTransition = (text: string) => {
  return Object.values(transitionsEnum).some((transition: any) => {
    return text.includes(transition);
  });
};

const checkSlugline = (text: string) => {
  return text.includes("EXT.") || text.includes("INT.");
};

const cleanScript = (text: string) => {
  return !(
    text.split(" ").length === 1 &&
    text.includes("CONTINUED:") &&
    text.trim() !== ""
  );
};

const parseType = (
  finalJson: any[],
  currentTextObj: any,
  stitchedText: string[],
  previousX: number,
  previousY: number
) => {
  const { x, y } = currentTextObj;
  let { text } = currentTextObj;

  // if width different
  if (Math.round(Math.abs(previousX - x))) {
    // and y different, than different section
    if (previousY != y) {
      previousX = x;
      previousY = y;

      if (stitchedText.length) {
        finalJson.push({ text: stitchedText });
      }

      stitchedText = [text.trim()];

      if (checkSlugline(text) || checkTransition(text)) {
        finalJson.push({ text: [text.trim()] });
        stitchedText = [];
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
        finalJson.push({ text: stitchedText });
      }
      if (cleanScript(text)) {
        finalJson.push({ text: [text.trim()] });
      }
      stitchedText = [];
    } else {
      if (cleanScript(text)) {
        stitchedText.push(text.trim());
      }
    }
    previousY = y;
  }

  return { finalJson, currentTextObj, stitchedText, previousX, previousY };
};

export const parseScriptTypes = (
  { finalJson, stitchedText, previousX, previousY }: IParseScriptTypes,
  currentTextObj: any
) => {
  if (
    !currentTextObj.hasOwnProperty("text") ||
    currentTextObj.text.trim() === ""
  ) {
    return { stitchedText, previousX, previousY };
  }

  const currResult = parseType(
    finalJson,
    currentTextObj,
    stitchedText,
    previousX,
    previousY
  );
  return {
    finalJson: currResult.finalJson,
    currentTextObj: currResult.currentTextObj,
    stitchedText: currResult.stitchedText,
    previousX: currResult.previousX,
    previousY: currResult.previousY
  };
};
