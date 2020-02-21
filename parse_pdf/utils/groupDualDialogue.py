import json


class GroupDualDialogue:
    def __init__(self, script):
        self.script = script["pdf"]
        self.newScript = []

    def detectDualDialogue(self):
        for page in self.script:
            x = {}
            self.newScript.append({"page": page["page"], "content": []})
            for i, content in enumerate(page["content"]):
                index = round(content["y"])
                if index in x:
                    # print(self.newScript[-1]["content"][x[index]])
                    # print(x[index])
                    self.newScript[-1]["content"][x[index]
                                                  ]["dialogue2"] = content["text"]
                else:
                    x[index] = len(self.newScript[-1]['content'])
                    self.newScript[-1]["content"].append(content)

    def groupDualDialogue(self, pageWidth):
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
                            if content["x"] < (pageWidth / 2):
                                currScript[-1]["content"][currScriptLen]["text"] += content["text"]
                            currScript[-1]["content"][currScriptLen]["dialogue2"] += content["text"]
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
