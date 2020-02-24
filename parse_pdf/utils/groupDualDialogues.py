import json


class GroupDualDialogues:
    def __init__(self, script):
        self.script = script["pdf"]
        self.newScript = []

    def detectDualDialogue(self):
        for page in self.script:
            existingY = {}
            self.newScript.append({"page": page["page"], "content": []})
            for i, content in enumerate(page["content"]):
                index = round(content["y"])
                if index in existingY:

                    # determine ordering of character2 and parent
                    swap = self.newScript[-1]["content"][existingY[index]]["segment"]
                    if swap["x"] > content["x"]:
                        self.newScript[-1]["content"][existingY[index]
                                                      ]["segment"] = content
                        self.newScript[-1]["content"][existingY[index]
                                                      ]["character2"] = swap
                    else:
                        self.newScript[-1]["content"][existingY[index]
                                                      ]["character2"] = content
                else:
                    existingY[index] = len(self.newScript[-1]['content'])
                    self.newScript[-1]["content"].append({
                        "segment": content
                    })

    def groupDualDialogues(self):
        self.detectDualDialogue()
        currScript = []
        for page in self.newScript:
            currScript.append({"page": page["page"], "content": []})
            margin = -1
            for i, content in enumerate(page["content"]):
                # if potentially dual
                if margin > 0:
                    currScriptLen = len(currScript[-1]["content"]) - 1
                    if "character2" not in content:
                        if content["segment"]["y"] - page["content"][i-1]["segment"]["y"] <= margin:
                            leftSide = abs(
                                content["segment"]["x"] - currScript[-1]["content"][currScriptLen]["segment"]["x"])
                            rightSide = abs(
                                content["segment"]["x"] - currScript[-1]["content"][currScriptLen]["character2"]['x'])
                            if leftSide < rightSide:
                                currScript[-1]["content"][currScriptLen]["segment"]["text"] += content["segment"]["text"]
                            else:
                                currScript[-1]["content"][currScriptLen]["character2"]["text"] += content["segment"]["text"]
                        else:
                            currScript[-1]['content'].append(content)
                            margin = 0
                    else:
                        currScript[-1]["content"].append(content)

                # if no dual
                else:
                    if "character2" in content:
                        margin = page["content"][i +
                                                 1]["segment"]["y"] - content["segment"]["y"]
                    currScript[-1]['content'].append(content)

        self.newScript = currScript
