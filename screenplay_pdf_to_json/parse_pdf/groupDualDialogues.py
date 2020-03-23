from screenplay_pdf_to_json.utils import isCharacter
import json
import copy

LATEST_PAGE = -1
EPSILON = 3


def groupDualDialogues(script, pageStart):
    """detects and groups dual dialogues"""

    newScript = []
    for page in script:
        if page["page"] < pageStart:
            continue
        newScript.append({"page": page["page"], "content": []})

        i = 0
        isDualDialogue = 0

        while i < len(page["content"]):
            content = page["content"][i]
            currentY = round(content["y"])
            segmentToAdd = [{
                "x": content["x"],
                "y": content["y"],
                "text": content["text"]
            }]

            nextContent = page["content"][i +
                                          1] if i + 1 < len(page["content"]) else False

            # if content's y axis is the same as
            if nextContent and isCharacter(content) and isCharacter(nextContent):
                isDualDialogue = 1

            if nextContent and currentY == nextContent["y"] and isDualDialogue > 0:
                character2ToAdd = {
                    "x": nextContent["x"],
                    "y": nextContent["y"],
                    "text": nextContent["text"]
                }
                left = segmentToAdd[0]
                right = character2ToAdd
                if left["x"] > nextContent["x"]:
                    right = left
                    left = copy.copy(right)

                if isDualDialogue <= 2:
                    newScript[-1]["content"].append({
                        "segment": [left],
                        "character2": [right]
                    })
                else:
                    newScript[-1]["content"][-1]["segment"].append(left)
                    newScript[-1]["content"][-1]["character2"].append(right)
                i += 1
                isDualDialogue += 1

            # if content resides in a different y axis, we know it's not part of a dual dialogue
            else:
                isDualDialogue = 0
                # add content's y axis as key and the content array index position as value
                newScript[-1]["content"].append({
                    "segment": segmentToAdd
                })
            i += 1

    newScript = stitchLastDialogue(newScript, pageStart)
    return newScript


def stitchLastDialogue(script, pageStart):
    """
    detect last line of a dual dialogue. This isn't detected by detectDualDialogue since
    a dialogue may be longer than the other, and therefore take up a different y value
    """
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
