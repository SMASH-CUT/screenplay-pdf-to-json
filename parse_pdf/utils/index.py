import json

from groupLines import ParsePdfClass
from groupDualDialogue import GroupDualDialogue
from groupSections import GroupSections

p1 = ParsePdfClass('../../script_assets/spiderverse.pdf')
p1.parsepdf()
p2 = GroupDualDialogue(p1.jsonScript)
p2.groupDualDialogue(p1.pageWidth)
p3 = GroupSections(p2.newScript)
p3.groupSections()
# print(type(p3.newScript))

# file1 = io.open("result.json", "w", encoding='utf-8')
file1 = open('result.json', 'w+')
json.dump(p3.newScript, file1, indent=4, ensure_ascii=False)
