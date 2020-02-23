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

                    # determine ordering of dialogue2 and parent
                    swap = self.newScript[-1]["content"][existingY[index]]
                    if swap["x"] > content["x"]:
                        self.newScript[-1]["content"][existingY[index]] = content
                        self.newScript[-1]["content"][existingY[index]
                                                      ]["dialogue2"] = swap
                    else:
                        self.newScript[-1]["content"][existingY[index]
                                                      ]["dialogue2"] = content
                else:
                    existingY[index] = len(self.newScript[-1]['content'])
                    self.newScript[-1]["content"].append(content)

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
                    if "dialogue2" not in content:
                        if content["y"] - page["content"][i-1]["y"] <= margin:
                            if abs(content["x"] - currScript[-1]["content"][currScriptLen]["x"]) < abs(content["x"] - currScript[-1]["content"][currScriptLen]["dialogue2"]['x']):
                                currScript[-1]["content"][currScriptLen]["text"] += content["text"]
                            else:
                                currScript[-1]["content"][currScriptLen]["dialogue2"]["text"] += content["text"]
                        else:
                            currScript[-1]['content'].append(content)
                            margin = 0
                    else:
                        currScript[-1]["content"].append(content)

                # if no dual
                else:
                    if "dialogue2" in content:
                        margin = page["content"][i+1]["y"] - content["y"]
                    currScript[-1]['content'].append(content)

        self.newScript = currScript
