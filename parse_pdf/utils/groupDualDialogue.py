import json

class GroupDualDialogue:
    def __init__(self, script):
        self.script = script["pdf"]
        self.newScript = []

    def detectDualDialogue(self):
        for page in self.script:
            x = {}
            self.newScript.append({ "page": page["page"], "content": [] })
            for i, content in enumerate(page["content"]):
                index = round(content["y"])
                if index in x:
                    # print(self.newScript[-1]["content"][x[index]])
                    # print(x[index])
                    self.newScript[-1]["content"][x[index]].append(content)
                else:
                    x[index] = len(self.newScript[-1]['content'])
                    self.newScript[-1]["content"].append([content])

    def groupDualDialogue(self):
        self.detectDualDialogue();
        oof = [];
        for page in self.newScript:
            oof.append({ "page": page["page"], "content": [] })
            margin = -1
            for i, content in enumerate(page["content"]):
                if margin > 0:
                    if len(content) == 1:
                        if content[0]["y"] - page["content"][i-1][0]["y"] <= margin:
                            oofLen = len(oof[-1]["content"]) - 1
                            # print("{}, page {}".format(oof[-1]["content"], page["page"]))
                            oof[-1]["content"][oofLen].append(content)
                        else:
                            oof[-1]["content"].append(content)
                            margin = 0
                    else:
                        oof[-1]["content"].append(content)
                else:        
                    if len(content) == 2:
                        margin = page["content"][i+1][0]["y"] - content[0]["y"]
                    oof[-1]['content'].append(content)

               
        self.newScript = oof
            
