import json
import re

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


class GroupSections:
    def __init__(self, script):
        self.script = script
        self.newScript = []

    @staticmethod
    def checkTransition(text):
        for transition in transitionEnum:
            if transition in text:
                return True
        return False

    @staticmethod
    def checkSlugline(text):
        return "EXT." in text or "INT." in text

    def cleanScript(self, text):
        return "CONTINUED:" not in text or "(CONTINUED)" not in text or text.strip() == ""

    @staticmethod
    def detectUnfinishedSentence(lastSentence):
        if (
            len(lastSentence) > 0 and not (GroupSections.checkSlugline(lastSentence) and GroupSections.checkTransition(lastSentence)) and
            lastSentence[len(lastSentence) - 1] != "." and
            lastSentence[len(lastSentence) - 1] != ")" and
            lastSentence[len(lastSentence) - 1] != "-" and
            lastSentence[len(lastSentence) - 1] != "?" and
            lastSentence[len(lastSentence) - 1] != "!"
        ):
            return True
        return False

    def groupSections(self):
        scriptSections = []

        for page in self.script:
            previousX = page["content"][0]["segment"]["x"] if len(
                page["content"]) > 1 else -1
            previousY = page["content"][0]["segment"]["y"] if len(
                page["content"]) > 1 else -1
            currentPageSections = ""
            scriptSections.append({"page": page["page"], "content": []})

            for i, content in enumerate(page["content"]):
                if "character2" in content:
                    if len(currentPageSections):
                        scriptSections[-1]["content"].append({
                            "segment": {
                                "text": currentPageSections,
                                "x": previousX,
                                "y": previousY
                            }
                        })
                    scriptSections[-1]["content"].append(content)
                    previousX = -1
                    previousY = -1
                    currentPageSections = ""
                    continue

                x = content["segment"]["x"]
                y = content["segment"]["y"]
                text = content["segment"]["text"]

                # check if pag enumber
                if re.search(r"^\d{1,3}\.$", content["segment"]["text"].strip()):
                    previousY = page["content"][i+1]["segment"]["y"] if len(
                        page["content"]) > i + 1 else -999
                    previousX = page["content"][i+1]["segment"]["x"] if len(
                        page["content"]) > i + 1 else -999
                    continue

                if round(abs(previousX - x)) > 0:
                    if previousY != y:
                        if len(currentPageSections) > 0:
                            scriptSections[-1]["content"].append({
                                "segment": {
                                    "text": currentPageSections,
                                    "x": previousX,
                                    "y": previousY
                                }
                            })
                            currentPageSections = ""

                            if GroupSections.checkSlugline(text) or GroupSections.checkTransition(text):
                                scriptSections[-1]["content"].append({
                                    "segment": {
                                        "text": content["segment"]["text"],
                                        "x": x,
                                        "y": y
                                    }
                                })
                                currentPageSections = ""
                            elif (self.cleanScript(text)):
                                currentPageSections = text.strip()
                        else:
                            if self.cleanScript(text):
                                currentPageSections = text.strip()

                        previousX = x
                        previousY = y
                    else:
                        if self.cleanScript(text):
                            currentPageSections = text.strip()
                        previousX = min(x, previousX)
                else:
                    if GroupSections.checkSlugline(text) or GroupSections.checkTransition(text):
                        if len(currentPageSections):
                            scriptSections[-1]["content"].append({
                                "segment": {
                                    "text": currentPageSections,
                                    "x": previousX,
                                    "y": previousY
                                }
                            })
                        if self.cleanScript(text):
                            scriptSections[-1]["content"].append({
                                "segment": {
                                    "text": content["segment"]["text"].strip(),
                                    "x": x,
                                    "y": y
                                }
                            })
                        currentPageSections = ""
                    elif self.cleanScript(text):
                        currentPageSections += text.strip()
                        previousY = y

            if len(currentPageSections) > 0:
                scriptSections[-1]["content"].append({
                    "segment": {
                        "text": currentPageSections,
                        "x": previousX,
                        "y": previousY
                    }
                })
        # print(scriptSections)
        self.newScript = scriptSections
