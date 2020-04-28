import re
from screenplay_pdf_to_json.utils.headingHelpers import isHeading
from screenplay_pdf_to_json.utils.characterHelpers import isCharacter


def cleanPage(script, pageStart):
    dialogueStitch = []
    for page in script:
        if page["page"] < pageStart:
            continue
        dialogueStitch.append({"page": page["page"], "content": []})

        firstRound = []
        for content in page["content"]:
            text = re.sub("\s{2}", " ", content["text"].strip())
            if text == "" or text == "*" or text == "." or text == "\\." or text == "\\" or text == "'":
                continue
            if content["x"] < 65 or content["x"] > 500 or content["y"] <= 50:
                continue
            content["text"] = text
            firstRound.append(content)

        for i, content in enumerate(firstRound):
            text = content["text"]
            if "Okay, so how many trees are on tha" in text:
                x = 0
            if not isHeading(content) and content["y"] < 80 and content["x"] < 100:
                if "TV Calling - For educational purposes only" in text:
                    continue
                elif (re.search(' \d{1,3}[.]?', text) or re.search('\d{1,2}\/\d{1,2}\/\d{2,4}', text)) and (i == 0 or i == len(content)-1):
                    continue
                elif (re.match('(\d|l|i|I){1,3}[.]?(?![\w\d])', text)) and len(text.strip()) < 5:
                    continue
                elif re.search(r"^i{2,3}$", text) and (len(text) < 2 or i == 0 or i == len(content)-1):
                    continue
                elif re.search(r"([(]?CONTINUED[:)]{1,2})", text):
                    continue
                elif re.match('i{2,3}', text):
                    continue

            dialogueStitch[-1]["content"].append(content)
    removeDuplicates(dialogueStitch)
    return dialogueStitch


def removeDuplicates(script):
    for pageIndex, page in enumerate(script):
        for contentIndex, content in enumerate(page["content"]):
            if contentIndex + 1 < len(page["content"]) and content == page["content"][contentIndex+1]:
                script[pageIndex]["content"].pop(contentIndex+1)
