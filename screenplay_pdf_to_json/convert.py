import json
import argparse
import pprint

from screenplay_pdf_to_json.parse_pdf import ParsePdfClass, groupDualDialogues, groupSections, sortLines, cleanPage, getTopTrends, stitchSeperateWordsIntoLines, processInitialPages

pp = pprint.PrettyPrinter(indent=4)


def convert(scriptFile, pageStart):
    # parse script based on pdfminer.six. Lacking documentation so gotta need some adjustments in our end :(
    p1 = ParsePdfClass(scriptFile)
    p1.parsepdf()
    newScript = p1.newScript["pdf"]

    firstPagesDict = processInitialPages(newScript)

    firstPages = firstPagesDict[0]
    skipPage = pageStart if pageStart else firstPagesDict[1]

    # remove any useless line (page number, empty line, special symbols)
    newScript = cleanPage(newScript, skipPage)

    # sort lines by y. If y is the same, then sort by x
    newScript = sortLines(newScript, skipPage)

    # group dual dialogues into the same segments
    newScript = groupDualDialogues(newScript, skipPage)

    # because of pdfminer's imperfections, we have to stitch words into what's supposed to be part of the same line
    newScript = stitchSeperateWordsIntoLines(newScript, skipPage)

    topTrends = getTopTrends(newScript)
    # pp.pprint(topTrends)

    # # group into sections based on type
    newScript = groupSections(topTrends, newScript, skipPage)

    newScript = firstPages + newScript
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
