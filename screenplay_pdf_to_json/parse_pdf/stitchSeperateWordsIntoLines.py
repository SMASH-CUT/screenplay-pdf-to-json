from copy import copy


def stitchSeperateWordsIntoLines(script, pageStart):
    dialogueStitch = []

    def getJoinedText(textArr):
        return " ".join([x["text"]
                         for x in textArr])
    def segmentTextExists(x): return len(x) > 0 and len(
        x[-1]["text"]) > 0
    for page in script:
        if page["page"] < pageStart:
            continue
        dialogueStitch.append({"page": page["page"], "content": []})

        contentStitch = {
            "segment": []
        }

        for i, content in enumerate(page["content"]):
            if "character2" in content:
                if segmentTextExists(contentStitch["segment"]):
                    dialogueStitch[-1]["content"].append(copy(contentStitch))
                contentStitch = {
                    "segment": []
                }
                dialogueStitch[-1]["content"].append(content)
            elif i > 0 and content["segment"][0]["y"] == page["content"][i-1]["segment"][0]["y"]:
                contentStitch["segment"][-1]["text"] += " " + \
                    getJoinedText(content["segment"])
            else:
                if segmentTextExists(contentStitch["segment"]):
                    dialogueStitch[-1]["content"].append(copy(contentStitch))
                contentStitch = copy(content)

        if len(contentStitch["segment"]) > 0:
            dialogueStitch[-1]["content"].append(copy(contentStitch))

    return dialogueStitch
