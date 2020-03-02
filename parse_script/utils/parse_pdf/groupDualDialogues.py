import json

def groupDualDialogues(script, pageStart):
    newScript = []
    for page in script:
        if page["page"] < pageStart:
            continue
        existingY = {}
        newScript.append({"page": page["page"], "content": []})
        for i, content in enumerate(page["content"]):
            currentY = round(content["y"])
            segmentToAdd = [{
                "x": content["x"],
                "y": content["y"],
                "text": content["text"]
            }]

            # if content's y axis is the same as
            if currentY in existingY:
                swap = newScript[-1]["content"][existingY[currentY]
                                                        ]["segment"]

                # determining ordering between the two dialogues
                if swap[-1]["x"] > content["x"]:
                    newScript[-1]["content"][existingY[currentY]
                                                    ]["segment"] = segmentToAdd
                    newScript[-1]["content"][existingY[currentY]
                                                    ]["character2"] = swap
                else:
                    newScript[-1]["content"][existingY[currentY]
                                                    ]["character2"] = segmentToAdd

            # if content resides in a different y axis, we know it's not part of a dual dialogue
            else:
                # add content's y axis as key and the content array index position as value
                existingY[currentY] = len(newScript[-1]['content'])
                newScript[-1]["content"].append({
                    "segment": segmentToAdd
                })
    return newScript