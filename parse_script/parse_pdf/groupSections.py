import json
from utils.characterHelpers import isCharacter
from utils.headingHelpers import isHeading


def groupSections(topTrends, script, pageStart):
    newScript = categorizeSections(topTrends, script, pageStart)

    finalSections = []
    for page in newScript:
        if page["page"] < pageStart:
            continue
        finalSections.append({"page": page["page"], "content": []})

        for i, content in enumerate(page["content"]):
            finalSections[-1]["content"].append({
                "scene_heading": content["scene_heading"],
                "scene": []
            })
            j = 0
            while j < len(content["scene"]):
                scene = content["scene"][j]

                sectionSameTypeAsPrevious = j > 0 and scene["type"] == content["scene"][j-1]["type"]
                if scene["type"] == "CHARACTER":
                    finalSections[-1]["content"][-1]["scene"].append({
                        "character": scene["text"],
                        "dialogue": ""
                    })
                elif scene["type"] == "DIALOGUE" and content["scene"][j-1]["type"] == "CHARACTER":
                    finalSections[-1]["content"][-1]["scene"][-1]["dialogue"] += scene["text"]
                elif sectionSameTypeAsPrevious and scene["type"] == "DIALOGUE":
                    finalSections[-1]["content"][-1]["scene"][-1]["dialogue"] += " " + scene["text"]
                elif sectionSameTypeAsPrevious and scene["type"] == "ACTION":
                    finalSections[-1]["content"][-1]["scene"][-1]["content"].append(
                        scene["content"][0])
                else:
                    finalSections[-1]["content"][-1]["scene"].append(scene)

                j += 1
    return finalSections


def categorizeSections(topTrends, script, pageStart):
    finalSections = []
    for page in script:
        if page["page"] < pageStart:
            continue
        finalSections.append({"page": page["page"], "content": []})

        finalSections[-1]["content"].append({
            "scene_heading": finalSections[-2]["content"][-1]["scene_heading"] if len(finalSections) > 2 else None,
            "scene": []
        })

        characterOccurred = False
        for i, content in enumerate(page["content"]):
            if "character2" in content:
                finalSections[-1]["content"][-1]["scene"].append({
                    "type": "DUAL_DIALOGUE",
                    "character1": content["segment"],
                    "character2": content["character2"],
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

            if isHeading(content["segment"][0]):
                if len(finalSections[-1]["content"][-1]["scene"]) == 0:
                    finalSections[-1]["content"][-1] = {
                        "scene_heading": content,
                        "scene": []
                    }
                else:
                    finalSections[-1]["content"].append({
                        "scene_heading": content,
                        "scene": []
                    })
                characterOccurred = False
            elif isTransition:
                finalSections[-1]["content"][-1]["scene"].append({
                    "type": "TRANSITION",
                    "text": text,
                    "metadata": {
                        "x": x,
                        "y": y
                    }
                })
                characterOccurred = False
            elif abs(x - topTrends[0][0]) <= 15:
                finalSections[-1]["content"][-1]["scene"].append({
                    "type": "ACTION",
                    "content": [{"text": text, "x": x, "y": y}]
                })
                characterOccurred = False

            elif isCharacter(content["segment"][0]):
                finalSections[-1]["content"][-1]["scene"].append({
                    "type": "CHARACTER",
                    "text": text,
                    "metadata": {
                        "x": x,
                        "y": y
                    }
                })
                characterOccurred = True
            else:
                currentScene = finalSections[-1]["content"][-1]["scene"]

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
