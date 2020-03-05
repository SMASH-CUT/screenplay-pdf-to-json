import json
import copy


def groupDualDialogues(script, pageStart):
    newScript = []
    for page in script:
        if page["page"] < pageStart:
            continue
        newScript.append({"page": page["page"], "content": []})

        characterName = False
        i = 0
        while i < len(page["content"]):
            content = page["content"][i]
            currentY = round(content["y"])
            segmentToAdd = [{
                "x": content["x"],
                "y": content["y"],
                "text": content["text"]
            }]

            # if content's y axis is the same as
            if i + 1 < len(page["content"]) and currentY == page["content"][i+1]["y"]:
                if content["text"] == content["text"].upper() and "(" not in content["text"].strip()[0] and (
                    page["content"][i+1]["text"] == page["content"][i+1]["text"].upper(
                    ) and "(" not in page["content"][i+1]["text"].strip()[0]
                ):
                    characterName = True
                if characterName:
                    character2ToAdd = {
                        "x": page["content"][i+1]["x"],
                        "y": page["content"][i+1]["y"],
                        "text": page["content"][i+1]["text"]
                    }
                    left = segmentToAdd[0]
                    right = character2ToAdd
                    if left["x"] > page["content"][i+1]["x"]:
                        right = left
                        left = copy.copy(right)
                    newScript[-1]["content"].append({
                        "segment": [left],
                        "character2": [right]
                    })
                    i += 1
                else:
                    # add content's y axis as key and the content array index position as value
                    newScript[-1]["content"].append({
                        "segment": segmentToAdd
                    })
            # if content resides in a different y axis, we know it's not part of a dual dialogue
            else:
                characterName = False
                # add content's y axis as key and the content array index position as value
                newScript[-1]["content"].append({
                    "segment": segmentToAdd
                })
            i += 1
    return newScript
