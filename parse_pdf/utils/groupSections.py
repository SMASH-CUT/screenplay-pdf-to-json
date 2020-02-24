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
            previousX = page["content"][0]["segment"]["x"] if len(
                page["content"]) > 1 else -1
            previousY = page["content"][0]["segment"]["y"] if len(
                page["content"]) > 1 else -1
            currentPageSections = []
            scriptSections.append({"page": page["page"], "content": []})

            for i, content in enumerate(page["content"]):

                # check if pag enumber
                if re.search(r"^\d{1,3}\.$", content["segment"]["text"].strip()):
                    previousY = page["content"][i+1]["segment"]["y"] if len(
                        page["content"]) > i + 1 else -999
                    previousX = page["content"][i+1]["segment"]["x"] if len(
                        page["content"]) > i + 1 else -999
                    continue

                x = content["segment"]["x"]
                y = content["segment"]["y"]
                text = content["segment"]["text"]

                # if page["page"] == 6:
                #     print(content)
                #     print(previousX)
                #     print(previousY)
                #     print("---")

                if "character2" in content:
                    if len(currentPageSections):
                        scriptSections[-1]["content"].append({
                            "segment": {
                                "text": currentPageSections,
                                "x": previousX,
                                "y": previousY
                            }
                        })

                    character2 = {
                        "x": content["character2"]["x"],
                        "y": content["character2"]["y"],
                        "text": [content["character2"]["text"].strip()],
                    }

                    segment = {
                        "x": x,
                        "y": y,
                        "text": [text.strip()]
                    }

                    scriptSections[-1]["content"].append({
                        "segment": segment,
                        "character2": character2
                    })

                    currentPageSections = []
                    previousX = x
                    previousY = y
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

                            currentPageSections = []

                            if self.checkSlugline(text) or self.checkTransition(text):
                                scriptSections[-1]["content"].append({
                                    "segment": {
                                        "text": [content["segment"]["text"]],
                                        "x": x,
                                        "y": y
                                    }
                                })
                                currentPageSections = []
                            elif (self.cleanScript(text)):
                                currentPageSections = [text.strip()]
                        else:
                            if self.cleanScript(text):
                                currentPageSections = [text.strip()]

                        previousX = x
                        previousY = y
                    else:
                        if self.cleanScript(text):
                            currentPageSections = [text.strip()]
                        previousX = min(x, previousX)
                else:
                    if self.checkSlugline(text) or self.checkTransition(text):
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
                                    "text": [content["segment"]["text"].strip()],
                                    "x": x,
                                    "y": y
                                }
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
                            # add space when appending
                            currentPageSections[len(currentPageSections) - 1] = "{} {}".format(
                                currentPageSections[len(currentPageSections) - 1].strip(), text.strip())
                        else:
                            currentPageSections.append(text.strip())
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
