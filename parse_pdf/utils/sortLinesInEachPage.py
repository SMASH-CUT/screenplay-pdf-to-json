import json

class SortLinesClass:
    def __init__(self, script):
        self.script = script["pdf"]
        self.newScript = []

    def sortLines(self):
        for page in self.script:
            x = {}
            self.newScript.append({ "page": page["page"], "content": [] })
            for i, content in enumerate(page["content"]):
                index = round(content["y"])
                if index in x:
                    print(self.newScript[-1]["content"][x[index]])
                    print(x[index])
                    self.newScript[-1]["content"][x[index]].append(content)
                else:
                    x[index] = len(self.newScript[-1]['content'])
                    self.newScript[-1]["content"].append([content])
            
