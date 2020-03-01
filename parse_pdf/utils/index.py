import json

from groupLines import ParsePdfClass
from groupDualDialogues import GroupDualDialogues
from groupSections import GroupSections
from groupTypes import GroupTypes
from SortLines import SortLines
from tokenizeText import TokenizeText
from removePageNumbers import removePageNumbers

p1 = ParsePdfClass('../../script_assets/star_is_born.pdf')
p1.parsepdf()

newScript = p1.newScript["pdf"]
newScript = removePageNumbers(newScript)

file1 = open('../results/resultFirst.json', 'w+')
json.dump(newScript, file1, indent=4, ensure_ascii=False)

p2 = GroupDualDialogues(newScript)
p2.groupDualDialogues()


px = SortLines(p2.newScript)
px.sortLines()

file1 = open('../results/resultDual.json', 'w+')
json.dump(px.newScript, file1, indent=4, ensure_ascii=False)

p3 = GroupSections(px.newScript)
p3.groupSections()

file1 = open('../results/resultDebug.json', 'w+')
json.dump(p3.newScript, file1, indent=4, ensure_ascii=False)

p4 = GroupTypes(p3.newScript)
p4.groupTypes(p1.pageWidth)

# p5 = TokenizeText()
# p5.tokenizeText(p4.newScript)

file1 = open('../results/result.json', 'w+')
json.dump(p4.newScript, file1, indent=4, ensure_ascii=False)
