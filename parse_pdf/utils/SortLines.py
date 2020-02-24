

class SortLines:
    def __init__(self, script):
        self.script = script
        self.newScript = []

    def sortLines(self):
        for page in self.script:
            self.newScript.append({
                "page": page["page"],
                "content": []
            })
            self.newScript[-1]["content"] = page["content"]
            self.newScript[-1]["content"].sort(
                key=lambda curr: curr["segment"]["y"])
