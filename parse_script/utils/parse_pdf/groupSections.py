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


def checkTransition(text):
    for transition in transitionEnum:
        if transition in text:
            return True
    return False


def checkSlugline(text):
    return "EXT." in text or "INT." in text


def cleanScript(text):
    return "CONTINUED:" not in text or "(CONTINUED)" not in text or text.strip() == ""


def detectUnfinishedSentence(lastSentence):
    if (
        len(lastSentence) > 0 and not (checkSlugline(lastSentence) and checkTransition(lastSentence)) and
        lastSentence[len(lastSentence) - 1] != "." and
        lastSentence[len(lastSentence) - 1] != ")" and
        lastSentence[len(lastSentence) - 1] != "-" and
        lastSentence[len(lastSentence) - 1] != "?" and
        lastSentence[len(lastSentence) - 1] != "!"
    ):
        return True
    return False


def getJoinedText(textArr):
    return " ".join([x["text"]
                     for x in textArr]).strip()

# join text array for each dialogue into string


def joinTextToOneString(script, pageStart):
    groupedTextScript = []

    def curatedContent(textType, content):
        return {
            "x": content[textType][0]["x"],
            "y": [line["y"] for line in content[textType]],
            "text": getJoinedText(content[textType])
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


def stitchLastDialogue(script, pageStart):
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
                    print(content)
                    # margin between character head and FIRST line of dialogue
                    margin = abs(page["content"][i+1]["segment"][0]["y"] -
                                 content["segment"][LATEST_PAGE]["y"])
                    currScript[LATEST_PAGE]['content'].append(content)
                else:
                    currScript[LATEST_PAGE]['content'].append(content)

    return currScript


def groupRestOfDualDialogue(script, pageStart):
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


def groupGenericSections(script, pageStart):
    genericSections = []
    for page in script:
        if page["page"] < pageStart:
            continue
        previousX = page["content"][0]["segment"]["x"] if len(
            page["content"]) > 1 else -1
        previousY = page["content"][0]["segment"]["y"][0] if len(
            page["content"]) > 1 else -1
        currentPageSections = ""
        genericSections.append({"page": page["page"], "content": []})

        for i, content in enumerate(page["content"]):
            x = content["segment"]["x"]
            y = content["segment"]["y"][0]
            text = content["segment"]["text"]

            if "character2" in content:
                if len(currentPageSections):
                    genericSections[-1]["content"].append({
                        "segment": {
                            "text": currentPageSections,
                            "x": previousX,
                            "y": previousY
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
                previousX = -1
                previousY = -1
                currentPageSections = ""
                continue

            if round(abs(previousX - x)) > 40:
                if previousY != y:
                    if len(currentPageSections) > 0:
                        genericSections[-1]["content"].append({
                            "segment": {
                                "text": currentPageSections,
                                "x": previousX,
                                "y": previousY
                            }
                        })
                        currentPageSections = ""
                    if (cleanScript(text)):
                        currentPageSections = text

                    if checkSlugline(text) or checkTransition(text):
                        genericSections[-1]["content"].append({
                            "segment": {
                                "text": text,
                                "x": x,
                                "y": y
                            }
                        })
                        currentPageSections = ""

                    previousX = x
                    previousY = y
                else:
                    if cleanScript(text):
                        currentPageSections = text
                    previousX = min(x, previousX)
            else:

                if checkSlugline(text) or checkTransition(text):
                    if len(currentPageSections):
                        genericSections[-1]["content"].append({
                            "segment": {
                                "text": currentPageSections,
                                "x": previousX,
                                "y": previousY
                            }
                        })
                    currentPageSections = ""
                    if cleanScript(text):
                        # if it's a header and time includes a long modifier
                        if "(" in text and ")" not in text:
                            currentPageSections = text
                        else:
                            genericSections[-1]["content"].append({
                                "segment": {
                                    "text": text,
                                    "x": previousX,
                                    "y": previousY
                                }
                            })
                            currentPageSections = ""
                    previousY = y
                elif cleanScript(text):
                    if currentPageSections == "" or currentPageSections[-1] == " ":
                        currentPageSections += text.strip()
                    else:
                        currentPageSections += " " + text.strip()
                    previousY = min(previousY, y)

        if len(currentPageSections) > 0:
            genericSections[-1]["content"].append({
                "segment": {
                    "text": currentPageSections,
                    "x": previousX,
                    "y": previousY
                }
            })
    return genericSections


def groupSections(script, pageStart):
    newScript = stitchLastDialogue(script, pageStart)
    newScript = groupRestOfDualDialogue(newScript, pageStart)
    newScript = joinTextToOneString(newScript, pageStart)
    newScript = groupGenericSections(newScript, pageStart)
    return newScript
