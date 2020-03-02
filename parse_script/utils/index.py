import json
import argparse
import pprint

from parse_pdf.groupLines import ParsePdfClass
from parse_pdf.groupDualDialogues import groupDualDialogues
from parse_pdf.groupSections import groupSections
from parse_pdf.groupTypes import groupTypes
from parse_pdf.SortLines import sortLines
from parse_pdf.cleanPage import cleanPage


def getTrends(script):
    trends = {}
    for page in script:
        for section in page["content"]:
            roundedX = round(section["segment"]["x"])
            if roundedX not in trends:
                trends[roundedX] = 1
            else:
                trends[roundedX] += 1
    return trends


pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Parse Screenplay PDF into JSON')
parser.add_argument('-s', metavar='screenplay', type=str,
                    help='screenplay PDF filename', required=True)

parser.add_argument('--start', metavar='start page', type=int,
                    help='page to begin analyzing', required=False)

args = parser.parse_args()
pageStart = args.start if args.start else 0

p1 = ParsePdfClass('../../script_assets/{}'.format(args.s))
p1.parsepdf()

newScript = p1.newScript["pdf"]
newScript = cleanPage(newScript, pageStart)

file1 = open('../results/resultFirst.json', 'w+')
json.dump(newScript, file1, indent=4, ensure_ascii=False)

newScript = groupDualDialogues(newScript, pageStart)
newScript = sortLines(newScript, pageStart)

file1 = open('../results/resultDual.json', 'w+')
json.dump(newScript, file1, indent=4, ensure_ascii=False)

newScript = groupSections(newScript, pageStart)

file1 = open('../results/resultDebug.json', 'w+')
json.dump(newScript, file1, indent=4, ensure_ascii=False)

experimentGetX = getTrends(newScript)
pp.pprint(experimentGetX)

newScript = groupTypes(newScript, pageStart, p1.pageWidth)

file1 = open('../results/result.json', 'w+')
json.dump(newScript, file1, indent=4, ensure_ascii=False)
