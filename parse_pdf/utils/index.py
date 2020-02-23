import json

from groupLines import ParsePdfClass
from groupDualDialogues import GroupDualDialogues
from groupSections import GroupSections
from groupTypes import GroupTypes
from SortLines import SortLines

p1 = ParsePdfClass('../../script_assets/marriage_story.pdf')
p1.parsepdf()
p2 = GroupDualDialogues(p1.newScript)
p2.groupDualDialogues()

px = SortLines(p2.newScript)
px.sortLines()

file1 = open('resultDebug2.json', 'w+')
json.dump(p2.newScript, file1, indent=4, ensure_ascii=False)
# file0 = open('resultDebug.json', 'w+')
# json.dump(px.newScript, file0, indent=4, ensure_ascii=False)
# p3 = GroupSections(p2.newScript)
# p3.groupSections()
# # p4 = GroupTypes(p3.newScript)
# # p4.groupTypes()

# file1 = open('result.json', 'w+')
# json.dump(p3.newScript, file1, indent=4, ensure_ascii=False)
