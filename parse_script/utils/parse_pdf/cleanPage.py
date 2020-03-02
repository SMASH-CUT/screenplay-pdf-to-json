import re


def cleanPage(script, pageStart):
    dialogueStitch = []
    for page in script:
        if page["page"] < pageStart:
            continue
        dialogueStitch.append({"page": page["page"], "content": []})
        for i, content in enumerate(page["content"]):
            text = content["text"].strip()
            if i == 0 and re.search('^\d{1,3}[.]?$', text):
                continue
            elif text == "":
                continue
            elif re.search(r"^i{2,3}|([(]?CONTINUED[:)]?)$", text) and len(text.split()) <= 2:
                continue
            elif "TV Calling - For educational purposes only" in text:
                continue
            dialogueStitch[-1]["content"].append(content)
    removeDuplicates(dialogueStitch)
    return dialogueStitch


def removeDuplicates(script):
    for pageIndex, page in enumerate(script):
        for contentIndex, content in enumerate(page["content"]):
            if contentIndex + 1 < len(page["content"]) and content == page["content"][contentIndex+1]:
                script[pageIndex]["content"].pop(contentIndex+1)
