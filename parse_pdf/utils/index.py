import json

from determineLines import ParsePdfClass
from sortLinesInEachPage import SortLinesClass

p1 = ParsePdfClass('../../script_assets/spiderverse.pdf')
p1.parsepdf()
p2 = SortLinesClass(p1.jsonScript)
p2.sortLines()
# file1 = io.open("result.json", "w", encoding='utf-8')
file1 = open('result.json', 'w+')
json.dump(p2.newScript, file1, indent=4, ensure_ascii=False)