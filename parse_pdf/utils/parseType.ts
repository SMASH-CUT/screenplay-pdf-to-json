import { transitionsEnum } from "../enums/transitionsEnum";

interface IParseScriptTypes {
  finalJson: any[];
  stichedText: string;
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

const parseType = (
  finalJson: any[],
  currentTextObj: any,
  stichedText: string,
  previousX: number,
  previousY: number
) => {
  const { x, y } = currentTextObj;
  let { text } = currentTextObj;

  // if width different
  if (previousX != x) {
    // and y different, than different section
    if (previousY != y) {
      previousX = x;
      previousY = y;

      finalJson.push({ text: stichedText });
      stichedText = text;
    }

    // and y same, than same section
    else {
      previousX = Math.min(x, previousX);
      stichedText += text;
    }
  }
  // if width same and y different, then same section
  else if (previousY != y) {
    if (checkSlugline(text) || checkTransition(text)) {
      previousX = x;
      previousY = y;

      finalJson.push({ text: stichedText });
      finalJson.push({ text });
      stichedText = "";
    } else {
      previousY = y;
      stichedText += text;
    }
  }

  return { finalJson, currentTextObj, stichedText, previousX, previousY };
};

export const parseScriptTypes = (
  { finalJson, stichedText, previousX, previousY }: IParseScriptTypes,
  currentTextObj: any
) => {
  if (
    !currentTextObj.hasOwnProperty("text") ||
    currentTextObj.text.trim() === ""
  ) {
    return { stichedText, previousX, previousY };
  }

  const currResult = parseType(
    finalJson,
    currentTextObj,
    stichedText,
    previousX,
    previousY
  );
  return {
    finalJson: currResult.finalJson,
    currentTextObj: currResult.currentTextObj,
    stichedText: currResult.stichedText,
    previousX: currResult.previousX,
    previousY: currResult.previousY
  };
};
