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

EPSILON = 3
LATEST_PAGE = -1

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

    def getJoinedText(self, textArr):
        return " ".join([x["text"]
                         for x in textArr]).strip()

    # join text array for each dialogue into string
    def joinTextToOneString(self, script):
        groupedTextScript = []
        def curatedContent(textType, content):
            return {
                "x": content[textType][0]["x"],
                "y": content[textType][0]["y"],
                "text": self.getJoinedText(content[textType])
            }
        for page in script:
            groupedTextScript.append({"page": page["page"], "content": []})
            for i, content in enumerate(page["content"]):
                groupedTextScript[-1]["content"].append({ "segment": curatedContent("segment", content) })
                if "character2" in content:
                    groupedTextScript[-1]["content"][-1]["character2"] = curatedContent("character2", content)
        return groupedTextScript

    # detect last line of a dual dialogue. This isn't detected by detectDualDialogue since
    # a dialogue may be longer than the other, and therefore take up a different y value
    def stitchLastDialogue(self, script):
        currScript = []
        for page in script:
            currScript.append({"page": page["page"], "content": []})
            margin = -1
            for i, content in enumerate(page["content"]):
                # if margin > 0, then content is potentially a dual dialogue
                if margin > 0:
                    currScriptLen = len(currScript[LATEST_PAGE]["content"]) - 1

                    # content might be the last line of dual dialogue, or not
                    if "character2" not in content and i > 0:
                        # last line of a dual dialogue
                        if abs(content["segment"]["y"] - page["content"][i-1]["segment"]["y"]) <= margin + EPSILON:
                            # print(json.dumps(currScript, indent=4))
                            def getDiff(contentX, currX): return abs(
                                contentX - currX)

                            diffBetweenContentAndSegment = getDiff(
                                content["segment"]["x"], page["content"][i-1]["segment"]["x"])
                            diffBetweenContentAndCharacter2 = getDiff(
                                content["segment"]["x"], page["content"][i-1]["character2"]["x"]) if "character2" in page["content"][i-1] else -1

                            if diffBetweenContentAndSegment < diffBetweenContentAndCharacter2:
                                currScript[LATEST_PAGE]["content"][currScriptLen]["segment"]["text"] += content["segment"]["text"]
                            else:
                                currScript[LATEST_PAGE]["content"][currScriptLen]["character2"]["text"] += content["segment"]["text"]

                        # not a dual dialogue. fuk outta here!
                        else:
                            currScript[LATEST_PAGE]['content'].append(content)
                            margin = 0

                    # still a dual dialogue
                    else:
                        currScript[LATEST_PAGE]["content"].append(content)

                # if no dual
                else:
                    if "character2" in content:
                        # margin between character head and FIRST line of dialogue
                        margin = page["content"][i+1]["segment"]["y"] - \
                            content["segment"]["y"]
                    currScript[LATEST_PAGE]['content'].append(content)

        return currScript

    def groupRestOfDualDialogue(self, script):
        dialogueStitch = []
        for page in script:
            quest = 0
            toAppend = 0
            dialogueStitch.append({"page": page["page"], "content": []})

            for i, content in enumerate(page["content"]):
                if "character2" in content:
                    # character name
                    if quest <= 1:
                        dialogueStitch[-1]["content"].append(content)

                    # rest of dual dialogue
                    else:
                        latestDialogue = dialogueStitch[-1]["content"][-1]
                        latestDialogue["character2"]["text"] += content["character2"]["text"]
                        latestDialogue["segment"]["text"] += content["segment"]["text"]
                    quest += 1
                else:
                    quest = 0
                    dialogueStitch[-1]["content"].append(content)

        return dialogueStitch

    def groupGenericSections(self, script):
        genericSections = []
        for page in script:
            previousX = page["content"][0]["segment"]["x"] if len(
                page["content"]) > 1 else -1
            previousY = page["content"][0]["segment"]["y"] if len(
                page["content"]) > 1 else -1
            currentPageSections = ""
            genericSections.append({"page": page["page"], "content": []})

            for i, content in enumerate(page["content"]):
                if "character2" in content:
                    if len(currentPageSections):
                        genericSections[-1]["content"].append({
                            "segment": {
                                "text": currentPageSections,
                            }
                        })
                    genericSections[-1]["content"].append({
                        "text": content["text"]
                    })
                    previousX = -1
                    previousY = -1
                    currentPageSections = ""
                    continue

                x = content["segment"]["x"]
                y = content["segment"]["y"]
                text = content["segment"]["text"]

                # check if pag enumber
                if re.search(r"^\d{1,3}\.$", text):
                    previousY = page["content"][i+1]["segment"]["y"] if len(
                        page["content"]) > i + 1 else -999
                    previousX = page["content"][i+1]["segment"]["x"] if len(
                        page["content"]) > i + 1 else -999
                    continue

                if round(abs(previousX - x)) > 0:
                    if previousY != y:
                        if len(currentPageSections) > 0:
                            genericSections[-1]["content"].append({
                                "segment": {
                                    "text": currentPageSections,
                                }
                            })
                            currentPageSections = ""

                            if GroupSections.checkSlugline(text) or GroupSections.checkTransition(text):
                                genericSections[-1]["content"].append({
                                    "segment": {
                                        "text": text,
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
                            genericSections[-1]["content"].append({
                                "segment": {
                                    "text": currentPageSections,
                                }
                            })
                        if self.cleanScript(text):
                            genericSections[-1]["content"].append({
                                "segment": {
                                    "text": text,
                                }
                            })
                        currentPageSections = ""
                    elif self.cleanScript(text):
                        currentPageSections += text.strip()
                        previousY = y

            if len(currentPageSections) > 0:
                genericSections[-1]["content"].append({
                    "segment": {
                        "text": currentPageSections,
                    }
                })
        return genericSections

    def groupSections(self):
        self.newScript = self.joinTextToOneString(self.script)
        self.newScript = self.stitchLastDialogue(self.newScript)
        self.newScript = self.groupRestOfDualDialogue(self.newScript)
        self.newScript = self.groupGenericSections(self.newScript)
