import json
import re

from screenplay_pdf_to_json.utils import isCharacter, isParenthetical, extractCharacter, isHeading, extractHeading

LAST_SCENE = -2


def groupSections(topTrends, script, pageStart):
    """group types into the same sections"""

    newScript = categorizeSections(topTrends, script, pageStart)
    newScript = combineCategories(newScript, pageStart)
    newScript = divideParentheticals(newScript)
    return newScript


def divideParentheticals(newScript):
    """seperates parentheticals from dialogues"""

    for page in newScript:
        for i, section in enumerate(page["content"]):
            for j, scene in enumerate(section["scene"]):
                if scene["type"] == "CHARACTER":
                    scene["content"]["dialogue"] = getParenthetical(
                        scene["content"]["dialogue"])
                elif scene["type"] == "DUAL_DIALOGUE":
                    scene["content"]["character1"]["dialogue"] = getParenthetical(
                        scene["content"]["character1"]["dialogue"])
                    scene["content"]["character2"]["dialogue"] = getParenthetical(
                        scene["content"]["character2"]["dialogue"])
    return newScript


def getParenthetical(text):
    """splits dialogue string into list, seperating any containing parenthetical(s)"""

    return list(
        filter(lambda x: len(x.strip()) > 0, re.split(r'(\([^)]+\))', text))
    )


def combineCategories(newScript, pageStart):
    """combines consecutive sections with the same type"""

    finalSections = []
    for page in newScript:
        if page["page"] < pageStart:
            continue
        finalSections.append({"page": page["page"], "content": []})

        for i, content in enumerate(page["content"]):
            finalSections[-1]["content"].append({
                "scene_number": content["scene_number"],
                "scene_info": content["scene_info"],
                "scene": []
            })
            j = 0
            while j < len(content["scene"]):
                scene = content["scene"][j]

                sectionSameTypeAsPrevious = j > 0 and scene["type"] == content["scene"][j-1]["type"]
                if scene["type"] == "CHARACTER":
                    finalSections[-1]["content"][-1]["scene"].append({
                        "type": "CHARACTER",
                        "content": {
                            "character": scene["text"]["character"],
                            "modifier": scene["text"]["modifier"],
                            "dialogue": ""
                        }
                    })
                elif scene["type"] == "DUAL_DIALOGUE":
                    if isCharacter(scene["content"]["character1"][0]):
                        finalSections[-1]["content"][-1]["scene"].append({
                            "type": "DUAL_DIALOGUE",
                            "content": {
                                "character1": extractCharacter(scene["content"]["character1"][0]),
                                "character2":  extractCharacter(scene["content"]["character2"][0]),
                            }
                        })
                    else:
                        finalSections[-1]["content"][-1]["scene"][-1]["content"]["character1"]["dialogue"] = getJoinedText(
                            scene["content"]["character1"])
                        finalSections[-1]["content"][-1]["scene"][-1]["content"]["character2"]["dialogue"] = getJoinedText(
                            scene["content"]["character2"])

                elif scene["type"] == "DIALOGUE" and content["scene"][j-1]["type"] == "CHARACTER":
                    finalSections[-1]["content"][-1]["scene"][-1]["content"]["dialogue"] += scene["text"]
                elif sectionSameTypeAsPrevious and scene["type"] == "DIALOGUE":
                    finalSections[-1]["content"][-1]["scene"][-1]["content"]["dialogue"] += " " + scene["text"]
                elif sectionSameTypeAsPrevious and scene["type"] == "ACTION":
                    # if part of same paragraph, concat text
                    if (scene["content"][0]["y"] - finalSections[-1]["content"][-1]["scene"][-1]["content"][-1]["y"] <= 16):
                        finalSections[-1]["content"][-1]["scene"][-1]["content"][-1]["text"] += scene["content"][0]["text"]
                        finalSections[-1]["content"][-1]["scene"][-1]["content"][-1]["y"] = scene["content"][0]["y"]
                    # else, just append entire text
                    else:
                        finalSections[-1]["content"][-1]["scene"][-1]["content"].append(
                            scene["content"][0])
                else:
                    finalSections[-1]["content"][-1]["scene"].append(scene)

                j += 1
    return finalSections


def getJoinedText(textArr):
    return " ".join([arr["text"]
                     for arr in textArr])


def categorizeSections(topTrends, script, pageStart):
    """categorize lines into types"""

    finalSections = []
    sceneNumber = 0
    for page in script:
        if page["page"] < pageStart:
            continue
        finalSections.append({"page": page["page"], "content": []})

        finalSections[-1]["content"].append({
            "scene_number": sceneNumber,
            "scene_info": finalSections[LAST_SCENE]["content"][-1]["scene_info"] if len(finalSections) >= 2 else None,
            "scene": []
        })

        characterOccurred = False
        for i, content in enumerate(page["content"]):
            if "character2" in content:
                finalSections[-1]["content"][-1]["scene"].append({
                    "type": "DUAL_DIALOGUE",
                    "content": {
                        "character1": content["segment"],
                        "character2": content["character2"],
                    }
                })
                characterOccurred = False
                continue

            previousY = page["content"][i -
                                        1]["segment"][-1]["y"] if i > 0 else 0
            x = content["segment"][0]["x"]
            y = content["segment"][0]["y"]
            text = content["segment"][0]["text"]

            # booleans
            isTransition = content["segment"][0]["x"] >= 420 or "FADE IN:" in text
            isAction = abs(x - topTrends[0][0]) <= 15

            if isHeading(content["segment"][0]):
                sceneNumber += 1
                if len(finalSections[-1]["content"][-1]["scene"]) == 0:
                    finalSections[-1]["content"][-1] = {
                        "scene_number": sceneNumber,
                        "scene_info": extractHeading(content["segment"][0]["text"]),
                        "scene": []
                    }
                else:
                    finalSections[-1]["content"].append({
                        "scene_number": sceneNumber,
                        "scene_info": extractHeading(content["segment"][0]["text"]),
                        "scene": []
                    })
                characterOccurred = False
            elif isTransition:
                finalSections[-1]["content"][-1]["scene"].append({
                    "type": "TRANSITION",
                    "content": {
                        "text": text,
                        "metadata": {
                            "x": x,
                            "y": y
                        }
                    }
                })
                characterOccurred = False
            elif isAction:
                # if Heading is multi-line
                if i > 0 and len(finalSections[-1]["content"][-1]["scene"]) == 0 and y - page["content"][i-1]["segment"][-1]["y"] < 24:
                    finalSections[-1]["content"][-1]["scene_info"]["location"] += " " + text
                else:
                    finalSections[-1]["content"][-1]["scene"].append({
                        "type": "ACTION",
                        "content": [{"text": text, "x": x, "y": y}]
                    })
                    characterOccurred = False

            elif isCharacter(content["segment"][0]):
                finalSections[-1]["content"][-1]["scene"].append({
                    "type": "CHARACTER",
                    "text": extractCharacter(content["segment"][0]),
                    "metadata": {
                        "x": x,
                        "y": y
                    }
                })
                characterOccurred = True
            else:
                currentScene = finalSections[-1]["content"][-1]["scene"]

                # first line of page is never a dialogue
                if len(currentScene) == 0 or not characterOccurred:
                    finalSections[-1]["content"][-1]["scene"].append({
                        "type": "ACTION",
                        "content": [{"text": text, "x": x, "y": y}]
                    })

                else:
                    finalSections[-1]["content"][-1]["scene"].append({
                        "type": "DIALOGUE",
                        "text": text,
                        "metadata": {
                            "x": x,
                            "y": y
                        }
                    })

    return finalSections
