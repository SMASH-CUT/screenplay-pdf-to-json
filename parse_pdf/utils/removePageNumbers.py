import re


def removePageNumbers(script):
    dialogueStitch = []
    for page in script:
        dialogueStitch.append({"page": page["page"], "content": []})
        for content in page["content"]:
            text = content["text"]
            if re.search(r"^i{2,3}|(pg)?\d{1,3}[\.]*|([(]?CONTINUED[:)]?)$", text) and len(text.split()) <= 2:
                continue
            dialogueStitch[-1]["content"].append(content)
    removeDuplicates(dialogueStitch)
    return dialogueStitch


def removeDuplicates(script):
    for pageIndex, page in enumerate(script):
        for contentIndex, content in enumerate(page["content"]):
            if contentIndex + 1 < len(page["content"]) and content == page["content"][contentIndex+1]:
                script[pageIndex]["content"].pop(contentIndex+1)
