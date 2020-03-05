import json
import re
from parse_pdf.groupTypes import determineCharacter

transitionEnum = [
    "FADE IN",
    "FADE OUT",
    "FADE UP",
    "JUMP CUT",
    "MATCH CUT",
    "SMASH MATCH CUT",
    "MATCH DISSOLVE",
    "CUT",
    "DISSOLVE",
    "FLASH CUT",
    "FREEZE FRAME",
    "IRIS IN",
    "IRIS OUT",
    "WIPE TO"
]

EPSILON = 3
LATEST_PAGE = -1


class GroupSections:
    previousX = 0
    previousY = 0
    upperCase = False
    currentPageSections = ""
    marginOfOperation = 999

    def checkTransition(self, text):
        for transition in transitionEnum:
            if transition in text:
                return True
        return False

    def checkSlugline(self, text):
        return "EXT." in text or "INT." in text

    def getJoinedText(self, textArr):
        return " ".join([x["text"]
                         for x in textArr]).strip()

    # join text array for each dialogue into string
    def joinTextToOneString(self, script, pageStart):
        groupedTextScript = []

        def curatedContent(textType, content):
            return {
                "x": content[textType][0]["x"],
                "y": [line["y"] for line in content[textType]],
                "text": self.getJoinedText(content[textType])
            }
        for page in script:
            if page["page"] < pageStart:
                continue
            groupedTextScript.append({"page": page["page"], "content": []})
            for i, content in enumerate(page["content"]):
                groupedTextScript[-1]["content"].append(
                    {"segment": curatedContent("segment", content)})
                if "character2" in content:
                    groupedTextScript[-1]["content"][-1]["character2"] = curatedContent(
                        "character2", content)
        return groupedTextScript

    # detect last line of a dual dialogue. This isn't detected by detectDualDialogue since
    # a dialogue may be longer than the other, and therefore take up a different y value
    def stitchLastDialogue(self, script, pageStart):
        currScript = []
        for page in script:
            if page["page"] < pageStart:
                continue
            currScript.append({"page": page["page"], "content": []})
            margin = -1
            for i, content in enumerate(page["content"]):
                # if margin > 0, then content is potentially a dual dialogue
                if margin > 0:
                    currScriptLen = len(currScript[LATEST_PAGE]["content"]) - 1

                    # content might be the last line of dual dialogue, or not
                    if "character2" not in content and i > 0:
                        # last line of a dual dialogue
                        if abs(content["segment"][0]["y"] - page["content"][i-1]["segment"][LATEST_PAGE]["y"]) <= margin + EPSILON:
                            def getDiff(contentX, currX): return abs(
                                contentX - currX)

                            diffBetweenContentAndSegment = getDiff(
                                content["segment"][0]["x"], currScript[LATEST_PAGE]["content"][currScriptLen]["segment"][0]["x"])
                            diffBetweenContentAndCharacter2 = getDiff(
                                content["segment"][0]["x"], currScript[LATEST_PAGE]["content"][currScriptLen]["character2"][0]["x"]) if "character2" in currScript[LATEST_PAGE]["content"][currScriptLen] else -1

                            if diffBetweenContentAndSegment < diffBetweenContentAndCharacter2:
                                currScript[LATEST_PAGE]["content"][currScriptLen]["segment"] += content["segment"]
                            else:
                                currScript[LATEST_PAGE]["content"][currScriptLen]["character2"] += content["segment"]

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
                        margin = abs(page["content"][i+1]["segment"][0]["y"] -
                                     content["segment"][LATEST_PAGE]["y"])
                        currScript[LATEST_PAGE]['content'].append(content)
                    else:
                        currScript[LATEST_PAGE]['content'].append(content)

        return currScript

    def groupRestOfDualDialogue(self, script, pageStart):
        dialogueStitch = []
        for page in script:
            if page["page"] < pageStart:
                continue
            quest = 0
            toAppend = 0
            dialogueStitch.append({"page": page["page"], "content": []})

            for i, content in enumerate(page["content"]):
                if "character2" in content:
                    # character name
                    if (determineCharacter(page["content"][i+1]["segment"][0] if i+1 < len(content) else None, content["segment"][0], i)):
                        dialogueStitch[-1]["content"].append(content)
                        quest = 0
                    elif quest <= 1:
                        dialogueStitch[-1]["content"].append(content)

                        # rest of dual dialogue
                    else:
                        latestDialogue = dialogueStitch[-1]["content"][-1]
                        latestDialogue["character2"] += content["character2"]
                        latestDialogue["segment"] += content["segment"]
                    quest += 1
                else:
                    quest = 0
                    dialogueStitch[-1]["content"].append(content)

        return dialogueStitch

    def groupGenericSections(self, script, pageStart):
        genericSections = []

        def stitchOrSeperateText(x, y, index, text, page, lowerMode):
            lengthSufficient = len(self.currentPageSections) > 0

            # if last text is ")", it's a paren, and so we want to combine it with current text
            notPartOfParentheses = ((")" != page["content"][index-1]["segment"]["text"][-1]
                                     and "(" != text[0]) or self.upperCase == True)

            outsideBoundary = y - self.previousY > self.marginOfOperation + 5

            if notPartOfParentheses and lengthSufficient and (self.upperCase == lowerMode or outsideBoundary):
                if "here today" in text:
                    print(text)
                    print("{}, {}, {}, {}".format(notPartOfParentheses,
                                                  lengthSufficient, abs(x - page["content"][index-1]["segment"]
                                                                        ["x"]) > 35, y - self.previousY > self.marginOfOperation + 5))
                genericSections[-1]["content"].append({
                    "segment": {
                        "text": self.currentPageSections,
                        "x": self.previousX,
                        "y": self.previousY
                    }
                })
                self.currentPageSections = ""
                self.marginOfOperation = page["content"][index+1]["segment"]["y"][0] - \
                    y if index + 1 < len(page["content"]) else 999

            addSpace = "" if self.currentPageSections == "" else " "
            self.currentPageSections += addSpace + text
            self.previousX = min(self.previousX, x)
            self.previousY = y

        for page in script:
            if page["page"] < pageStart:
                continue
            self.previousX = page["content"][0]["segment"]["x"] if len(
                page["content"]) > 1 else -1
            self.previousY = page["content"][0]["segment"]["y"][0] if len(
                page["content"]) > 1 else -1
            self.currentPageSections = ""
            genericSections.append({"page": page["page"], "content": []})

            self.upperCase = False
            self.marginOfOperation = 999
            for i, content in enumerate(page["content"]):
                x = content["segment"]["x"]
                y = content["segment"]["y"][0]
                text = content["segment"]["text"]

                if "character2" in content:
                    if len(self.currentPageSections):
                        genericSections[-1]["content"].append({
                            "segment": {
                                "text": self.currentPageSections,
                                "x": self.previousX,
                                "y": self.previousY
                            }
                        })
                    genericSections[-1]["content"].append({
                        "segment": {
                            "text": content["segment"]["text"],
                            "x": x,
                            "y": y
                        },
                        "character2": {
                            "text": content["character2"]["text"]
                        },
                    })
                    self.previousX = -1
                    self.previousY = -1
                    self.currentPageSections = ""
                    continue

                if text == text.upper():
                    stitchOrSeperateText(x, y, i, text, page, False)
                    self.upperCase = True
                else:
                    stitchOrSeperateText(x, y, i, text, page, True)
                    self.upperCase = False

            if len(self.currentPageSections) > 0:
                genericSections[-1]["content"].append({
                    "segment": {
                        "text": self.currentPageSections,
                        "x": self.previousX,
                        "y": self.previousY
                    }
                })
        return genericSections

    def groupSections(self, script, pageStart):
        newScript = self.stitchLastDialogue(script, pageStart)
        newScript = self.groupRestOfDualDialogue(newScript, pageStart)
        newScript = self.joinTextToOneString(newScript, pageStart)
        newScript = self.groupGenericSections(newScript, pageStart)
        return newScript
