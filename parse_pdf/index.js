const fs = require('fs');
const pdf = require('pdf-parse');

import { renderText } from './utils/renderText'

let dataBuffer = fs.readFileSync('../script_assets/script1.pdf');

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
    fs.writeFileSync('./results/script.json', data.text);
});
