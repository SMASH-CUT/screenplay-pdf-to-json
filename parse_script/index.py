import json
import argparse
import pprint

from parse_pdf.groupLines import ParsePdfClass
from parse_pdf.groupDualDialogues import groupDualDialogues
from parse_pdf.groupSections import groupSections
from parse_pdf.SortLines import sortLines
from parse_pdf.cleanPage import cleanPage
from parse_pdf.getTopTrends import getTopTrends
from parse_pdf.stitchSeperateWordsIntoLines import stitchSeperateWordsIntoLines


pp = pprint.PrettyPrinter(indent=4)

parser = argparse.ArgumentParser(description='Parse Screenplay PDF into JSON')
parser.add_argument('-s', metavar='screenplay', type=str,
                    help='screenplay PDF filename', required=True)

parser.add_argument('--start', metavar='start page', type=int,
                    help='page to begin analyzing', required=False)

# start from pageStart set up by user.  default to 0
args = parser.parse_args()
pageStart = args.start if args.start else 0

# parse script based on pdfminer.six. Lacking documentation so gotta need some adjustments in our end :(
p1 = ParsePdfClass(args.s)
p1.parsepdf()
newScript = p1.newScript["pdf"]

# remove any useless line (page number, empty line, special symbols)
newScript = cleanPage(newScript, pageStart)

file1 = open('results/resultFirst.json', 'w+')
json.dump(newScript, file1, indent=4, ensure_ascii=False)

# sort lines by y. If y is the same, then sort by x
newScript = sortLines(newScript, pageStart)
file1 = open('results/resultSort.json', 'w+')
json.dump(newScript, file1, indent=4, ensure_ascii=False)

# group dual dialogues into the same segments
newScript = groupDualDialogues(newScript, pageStart)

file1 = open('results/resultDual.json', 'w+')
json.dump(newScript, file1, indent=4, ensure_ascii=False)

# because of pdfminer's imperfections, we have to stitch words into what's supposed to be part of the same line
newScript = stitchSeperateWordsIntoLines(newScript, pageStart)

file1 = open('results/resultStitch.json', 'w+')
json.dump(newScript, file1, indent=4, ensure_ascii=False)

topTrends = getTopTrends(newScript)
pp.pprint(topTrends)

# # group into sections based on type
newScript = groupSections(topTrends, newScript, pageStart)

file1 = open('results/result.json', 'w+')
json.dump(newScript, file1, indent=4, ensure_ascii=False)
