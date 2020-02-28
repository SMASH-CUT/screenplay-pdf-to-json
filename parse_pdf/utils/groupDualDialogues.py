import json

from groupSections import GroupSections
from groupTypes import GroupTypes


class GroupDualDialogues:
    def __init__(self, script):
        self.script = script["pdf"]
        self.newScript = []

    def detectDualDialogue(self):
        for page in self.script:
            existingY = {}
            self.newScript.append({"page": page["page"], "content": []})
            for i, content in enumerate(page["content"]):
                currentY = round(content["y"])
                segmentToAdd = [{
                    "x": content["x"],
                    "y": content["y"],
                    "text": content["text"]
                }]

                # if content's y axis is the same as
                if currentY in existingY:
                    swap = self.newScript[-1]["content"][existingY[currentY]
                                                         ]["segment"]

                    # determining ordering between the two dialogues
                    if swap[-1]["x"] > content["x"]:
                        self.newScript[-1]["content"][existingY[currentY]
                                                      ]["segment"] = segmentToAdd
                        self.newScript[-1]["content"][existingY[currentY]
                                                      ]["character2"] = swap
                    else:
                        self.newScript[-1]["content"][existingY[currentY]
                                                      ]["character2"] = segmentToAdd

                # if content resides in a different y axis, we know it's not part of a dual dialogue
                else:
                    # add content's y axis as key and the content array index position as value
                    existingY[currentY] = len(self.newScript[-1]['content'])
                    self.newScript[-1]["content"].append({
                        "segment": segmentToAdd
                    })

    def groupDualDialogues(self):
        self.detectDualDialogue()
