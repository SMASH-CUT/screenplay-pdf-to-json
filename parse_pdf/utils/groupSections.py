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
                    currScriptLen = len(currScript[-1]["content"]) - 1

                    # content might be the last line of dual dialogue, or not
                    if "character2" not in content:
                        # last line of a dual dialogue
                        if abs(content["segment"][0]["y"] - page["content"][i-1]["segment"][-1]["y"]) <= margin + EPSILON:
                            # print(json.dumps(currScript, indent=4))
                            def getDiff(contentX, currX): return abs(
                                contentX - currX)
                            diffBetweenContentAndSegment = getDiff(
                                content["segment"][-1]["x"], currScript[-1]["content"][currScriptLen]["segment"][-1]["x"])
                            diffBetweenContentAndCharacter2 = getDiff(
                                content["segment"][-1]["x"], currScript[-1]["content"][currScriptLen]["character2"][-1]["x"])

                            if diffBetweenContentAndSegment < diffBetweenContentAndCharacter2:
                                segmentText = currScript[-1]["content"][currScriptLen]["segment"].append(
                                    content["segment"][-1])
                            else:
                                character2Text = currScript[-1]["content"][currScriptLen]["character2"].append(
                                    content["segment"][-1])

                        # not a dual dialogue. fuk outta here!
                        else:
                            currScript[-1]['content'].append(content)
                            margin = 0

                    # still a dual dialogue
                    else:
                        currScript[-1]["content"].append(content)

                # if no dual
                else:
                    if "character2" in content:
                        # margin between character head and FIRST line of dialogue
                        margin = page["content"][i+1]["segment"][0]["y"] - \
                            content["segment"][-1]["y"]
                    currScript[-1]['content'].append(content)

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
                        x = dialogueStitch[-1]["content"][-1]
                        x["character2"] += content["character2"]
                        x["segment"] += content["segment"]
                    quest += 1
                else:
                    quest = 0
                    dialogueStitch[-1]["content"].append(content)

        return dialogueStitch

    def groupSections(self):
        scriptSections = []

        self.newScript = self.stitchLastDialogue(self.script)
        self.newScript = self.groupRestOfDualDialogue(self.newScript)

        # for page in self.newScript:
        #     previousX = page["content"][0]["segment"]["x"] if len(
        #         page["content"]) > 1 else -1
        #     previousY = page["content"][0]["segment"]["y"] if len(
        #         page["content"]) > 1 else -1
        #     currentPageSections = ""
        #     scriptSections.append({"page": page["page"], "content": []})

        #     for i, content in enumerate(page["content"]):
        #         if "character2" in content:
        #             if len(currentPageSections):
        #                 scriptSections[-1]["content"].append({
        #                     "segment": {
        #                         "text": currentPageSections,
        #                         "x": previousX,
        #                         "y": previousY
        #                     }
        #                 })
        #             scriptSections[-1]["content"].append(content)
        #             previousX = -1
        #             previousY = -1
        #             currentPageSections = ""
        #             continue

        #         x = content["segment"]["x"]
        #         y = content["segment"]["y"]
        #         text = content["segment"]["text"]

        #         # check if pag enumber
        #         if re.search(r"^\d{1,3}\.$", content["segment"]["text"].strip()):
        #             previousY = page["content"][i+1]["segment"]["y"] if len(
        #                 page["content"]) > i + 1 else -999
        #             previousX = page["content"][i+1]["segment"]["x"] if len(
        #                 page["content"]) > i + 1 else -999
        #             continue

        #         if round(abs(previousX - x)) > 0:
        #             if previousY != y:
        #                 if len(currentPageSections) > 0:
        #                     scriptSections[-1]["content"].append({
        #                         "segment": {
        #                             "text": currentPageSections,
        #                             "x": previousX,
        #                             "y": previousY
        #                         }
        #                     })
        #                     currentPageSections = ""

        #                     if GroupSections.checkSlugline(text) or GroupSections.checkTransition(text):
        #                         scriptSections[-1]["content"].append({
        #                             "segment": {
        #                                 "text": content["segment"]["text"],
        #                                 "x": x,
        #                                 "y": y
        #                             }
        #                         })
        #                         currentPageSections = ""
        #                     elif (self.cleanScript(text)):
        #                         currentPageSections = text.strip()
        #                 else:
        #                     if self.cleanScript(text):
        #                         currentPageSections = text.strip()

        #                 previousX = x
        #                 previousY = y
        #             else:
        #                 if self.cleanScript(text):
        #                     currentPageSections = text.strip()
        #                 previousX = min(x, previousX)
        #         else:
        #             if GroupSections.checkSlugline(text) or GroupSections.checkTransition(text):
        #                 if len(currentPageSections):
        #                     scriptSections[-1]["content"].append({
        #                         "segment": {
        #                             "text": currentPageSections,
        #                             "x": previousX,
        #                             "y": previousY
        #                         }
        #                     })
        #                 if self.cleanScript(text):
        #                     scriptSections[-1]["content"].append({
        #                         "segment": {
        #                             "text": content["segment"]["text"].strip(),
        #                             "x": x,
        #                             "y": y
        #                         }
        #                     })
        #                 currentPageSections = ""
        #             elif self.cleanScript(text):
        #                 currentPageSections += text.strip()
        #                 previousY = y

        #     if len(currentPageSections) > 0:
        #         scriptSections[-1]["content"].append({
        #             "segment": {
        #                 "text": currentPageSections,
        #                 "x": previousX,
        #                 "y": previousY
        #             }
        #         })
        # # print(scriptSections)
        # self.newScript = scriptSections
