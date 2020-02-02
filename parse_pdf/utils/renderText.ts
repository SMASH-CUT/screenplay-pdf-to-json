interface IProcessText {
  parsedScript: any;
  text: any;
  prevY: any;
  prevX: any;
}

const processText = (
  { parsedScript, text, prevY, prevX }: IProcessText,
  item: any
) => {
  const x = item.transform[4];
  const y = item.transform[5];

  if (item.str.includes("EXT.") || item.str.includes("INT.")) {
    prevX = x;
    prevY = y;

    parsedScript.push({ text });
    text = item.str;
  } else {
    // if width different
    if (prevX != x) {
      // and y different, than different section
      if (prevY != y) {
        prevX = x;
        prevY = y;

        parsedScript.push({ text });
        text = item.str;
      }

      // and y same, than same section
      else {
        prevX = Math.min(x, prevX);
        text += item.str;
      }
    }
    // if width same and y different, then same section
    else if (prevY != y) {
      prevY = y;
      text += item.str;
    }
  }

  return { parsedScript, text, prevY, prevX };
};

export const renderText = (textContent: any) => {
  let result: any[] = [];

  if (!textContent.items.length) {
    return result;
  }

  const init = {
    parsedScript: [],
    text: "",
    prevY: textContent.items[0].transform[5],
    prevX: -999
  };
  result = textContent.items.reduce(processText, init);
  return result;
};
