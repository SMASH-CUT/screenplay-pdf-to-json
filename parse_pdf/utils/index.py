import json

from determineLines import ParsePdfClass
from groupDualDialogue import GroupDualDialogue

p1 = ParsePdfClass('../../script_assets/spiderverse.pdf')
p1.parsepdf()
p2 = GroupDualDialogue(p1.jsonScript)
p2.groupDualDialogue()
# file1 = io.open("result.json", "w", encoding='utf-8')
file1 = open('oof.json', 'w+')
json.dump(p2.newScript, file1, indent=4, ensure_ascii=False)