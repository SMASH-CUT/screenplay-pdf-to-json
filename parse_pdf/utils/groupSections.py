import json
import re


class GroupSections:
    def __init__(self, script):
        self.script = script
        self.newScript = []

    transitionEnum = {
        "FADE_IN": "FADE IN",
        "FADE_OUT": "FADE OUT",
        "FADE_UP": "FADE UP",
        "JUMP_CUT": "JUMP CUT",
        "MATCH_CUT": "MATCH CUT",
        "SMASH_CUT": "SMASH MATCH CUT",
        "MATCH_DISSOLVE": "MATCH DISSOLVE",
        "CUT": "CUT",
        "DISSOLVE": "DISSOLVE",
        "FLASH_CUT": "FLASH CUT",
        "FREEZE_FRAME": "FREEZE FRAME",
        "IRIS_IN": "IRIS IN",
        "IRIS_OUT": "IRIS OUT",
        "WIPE": "WIPE TO"
    }

    def checkTransition(self, text):
        for transition in self.transitionEnum:
            if transition in text:
                return True
        return False

    def checkSlugline(self, text):
        return "EXT." in text or "INT." in text

    def cleanScript(self, text):
        return "CONTINUED:" not in text or "(CONTINUED)" not in text or text.strip() == ""

    def groupSections(self):
        scriptSections = []

        for page in self.script:
            previousX = -1
            previousY = page["content"][0]["y"] if len(
                page["content"]) > 1 else -999
            currentPageSections = []
            scriptSections.append({"page": page["page"], "content": []})

            for i, content in enumerate(page["content"]):
                if re.search(r"^\d{1,3}\.$", content["text"].strip()):
                    previousY = page["content"][i+1]["y"] if len(
                        page["content"]) > 1 and len(page["content"]) > i + 1 else -999
                    continue
                x = content["x"]
                y = content["y"]
                text = content["text"]

                if "dialogue2" in content:
                    scriptSections[-1]["content"].append(content)

                if round(abs(previousX - x)) > 0:
                    if previousY != y:
                        if len(currentPageSections) > 0:
                            scriptSections[-1]["content"].append({
                                "text": currentPageSections,
                                "x": previousX,
                                "y": previousY
                            })

                            previousX = x
                            previousY = y
                            currentPageSections = []

                            if self.checkSlugline(text) or self.checkTransition(text):
                                scriptSections[-1]["content"].append(
                                    {"text": content["text"], "x": x, "y": y})
                                currentPageSections = []
                            elif (self.cleanScript(text)):
                                currentPageSections = [text.strip()]
                    else:
                        previousX = min(x, previousX)
                        if self.cleanScript(text):
                            currentPageSections.append(content["text"])
                else:
                    if self.checkSlugline(text) or self.checkTransition(text):
                        if len(currentPageSections):
                            scriptSections[-1]["content"].append({
                                "text": currentPageSections,
                                "x": previousX,
                                "y": previousY
                            })
                        if self.cleanScript(text):
                            scriptSections[-1]["content"].append({
                                "text": [content["text"].strip()],
                                "x": x,
                                "y": y
                            })
                        currentPageSections = []
                    elif self.cleanScript(text):
                        lastSentence = currentPageSections[len(currentPageSections) -
                                                           1] if len(currentPageSections) > 0 else ""
                        if (
                            len(lastSentence) > 0 and not (self.checkSlugline(lastSentence) and self.checkTransition(lastSentence)) and
                            lastSentence[len(lastSentence) - 1] != "." and
                            lastSentence[len(lastSentence) - 1] != ")" and
                            lastSentence[len(lastSentence) - 1] != "-"
                        ):
                            currentPageSections[len(currentPageSections) -
                                                1] += text.strip()
                        else:
                            currentPageSections.append(text.strip())
                    previousY = y

        # print(scriptSections)
        self.newScript = scriptSections
