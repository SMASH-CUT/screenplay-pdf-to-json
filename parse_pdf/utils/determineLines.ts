interface IProcessText {
  parsedScript: any;
  text: any;
  previousY: any;
  previousX: any;
}

const determineLine = (
  { parsedScript, text, previousY, previousX }: IProcessText,
  item: any
) => {
  const x = item.transform[4];
  const y = item.transform[5];

  if (y === previousY) {
    text += item.str;
  } else {
    parsedScript.push({ text, x: previousX, y: previousY });
    text = item.str;
    previousX = x;
    previousY = y;
  }

  return { parsedScript, text, previousY, previousX };
};

export const determineLines = (textContent: any) => {
  let result: any = [];
  if (!textContent.items.length) {
    return {};
  }
  const init = {
    parsedScript: [],
    text: "",
    previousY: textContent.items[0].transform[5],
    previousX: -999
  };

  result = textContent.items.reduce(determineLine, init);

  return result.parsedScript;
};
