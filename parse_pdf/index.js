const fs = require('fs');
const pdf = require('pdf-parse');

let dataBuffer = fs.readFileSync('../script_assets/script1.pdf');

let debug = [];

const processText = ({ parsedScript, text, prevY, prevX }, item) => {
    const x = item.transform[4];
    const y = item.transform[5];

    if (item.str.includes('EXT.') || item.str.includes('INT.')) {
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

    return { parsedScript, text, prevY, prevX }
};

const renderText = (textContent) => {
    debug = [
        ...debug,
        ...textContent.items
    ];
    let result = [];

    if (!textContent.items.length) {
        return result;
    }

    const init = {
        parsedScript: [],
        text: '',
        prevY: textContent.items[0].transform[5],
        prevX: -999
    }
    result = textContent.items.reduce(processText, init);
    return result;
}

// default render callback
const renderPage = async (pageData) => {
    //check documents https://mozilla.github.io/pdf.js/
    let render_options = {
        //replaces all occurrences of whitespace with standard spaces (0x20). The default value is `false`.
        normalizeWhitespace: true,
        //do not attempt to combine same line TextItem's. The default value is `false`.
        disableCombineTextItems: false
    }

    const renderResult = await pageData.getTextContent(render_options)
        .then((textContent) => renderText(textContent));

    return JSON.stringify(renderResult, null, 4);
}

let options = {
    pagerender: renderPage
}

pdf(dataBuffer, options).then((data) => {
    // fs.writeFileSync('analyze.json', JSON.stringify(debug, null, 4));
    fs.writeFileSync('script.json', data.text);
});
