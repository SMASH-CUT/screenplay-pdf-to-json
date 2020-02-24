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

p3 = GroupSections(px.newScript)
p3.groupSections()

# p4 = GroupTypes(p3.newScript)
# p4.groupTypes(p1.pageWidth)

file1 = open('../results/resultDebug.json', 'w+')
json.dump(p3.newScript, file1, indent=4, ensure_ascii=False)
