import json
import argparse

from screenplay_pdf_to_json.parse_pdf import parsePdf, groupDualDialogues, groupSections, sortLines, cleanPage, getTopTrends, stitchSeperateWordsIntoLines, processInitialPages

def convert(scriptFile, pageStart):
    # parse script based on pdfminer.six. Lacking documentation so gotta need some adjustments in our end :(
    newScript = parsePdf(scriptFile)["pdf"]

    file1 = open('./bibi.json', 'w+')
    json.dump(newScript, file1, indent=4, ensure_ascii=False)

    firstPagesDict = processInitialPages(newScript)

    firstPages = firstPagesDict["firstPages"]
    skipPage = pageStart if pageStart else firstPagesDict["pageStart"]

    # remove any useless line (page number, empty line, special symbols)
    newScript = cleanPage(newScript, skipPage)

    file1 = open('./bibi.json', 'w+')
    json.dump(newScript, file1, indent=4, ensure_ascii=False)

    # sort lines by y. If y is the same, then sort by x
    newScript = sortLines(newScript, skipPage)

    # group dual dialogues into the same segments
    newScript = groupDualDialogues(newScript, skipPage)


    # because of pdfminer's imperfections, we have to stitch words into what's supposed to be part of the same line
    newScript = stitchSeperateWordsIntoLines(newScript, skipPage)

    
    topTrends = getTopTrends(newScript)

    # group into sections based on type
    newScript = groupSections(topTrends, newScript, skipPage)

    newScript = firstPages + newScript
    scriptFile.close()
    return newScript


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Parse Screenplay PDF into JSON')

    parser.add_argument('-s', metavar='screenplay', type=str,
                        help='screenplay PDF filename', required=True)

    parser.add_argument('--start', metavar='start page', type=int,
                        help='page to begin analyzing', required=False)

    # start from skipPage set up by user.  default to 0
    args = parser.parse_args()
    scriptFile = open(args.s, 'rb')
    pageStart = args.start
    newScript = convert(scriptFile, pageStart)
    file1 = open('./result.json', 'w+')
    json.dump(newScript, file1, indent=4, ensure_ascii=False)
