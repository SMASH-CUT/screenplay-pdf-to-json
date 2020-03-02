import copy
import json
import re
import spacy

nlp = spacy.load("en_core_web_sm")


headingEnum = ["EXT./INT.", "INT./EXT.", "INT.", "EXT."]


def determineHeading(textStr):
    for heading in headingEnum:
        if heading in textStr:
            return True
    return False


def extractTime(textStr):
    findTime = re.search(
        '[-,]?[ ]?(DAWN|DUSK|((LATE|EARLY) )?(NIGHT|AFTERNOON|MORNING)|DAYS|DAY|NIGHT|DAYS|DAY|LATER|NIGHT|SAME|CONTINUOUS|(MOMENTS LATER))', textStr)
    return findTime.start() if findTime else None


def determineCharacter(nextContent, currentContent,  i):
    textStr = currentContent["text"]
    x = currentContent["x"]
    y = currentContent["y"]
    characterNameEnum = ["V.O", "O.S", "CONT'D"]

    if nextContent:
        if nextContent["y"] - y > 40:
            return False

    for heading in characterNameEnum:
        if heading in textStr:
            return True

    if not textStr[0].isalpha():
        return False

    if textStr != textStr.upper():
        return False

    if " BY" in textStr:
        return False

    doc = nlp(textStr)
    for token in doc:
        if token.pos_ == "VERB" or token.pos_ == "DET":
            return False

    # check if header?
    if "--" in textStr or " - " in textStr or ":" in textStr or "." in textStr[-1]:
        return False

    # if not re.search('^[a-zA-Z]+(([\',. -][a-zA-Z ])?[a-zA-Z]*)*$', textStr):
    #     return False
    if "END" in textStr or "INC." in textStr:
        return False

    return True


def containsParentheticals(text):
    return "(" in text[0] and ")" in text[-1]


def containsDialogue(text, y, upperY, x, correctMargin, correctWidth):
    return text.upper() != text and abs(abs(upperY - y) - correctMargin) < 5 and abs(x - correctWidth) < 30


def extractCharacter(scene, content, i):
    def generateCharacterType(content, index, characterType):
        textStr = content[index][characterType]["text"]
        split = content[index][characterType]["text"].split()
        character = list(
            filter(lambda x: True if "(" not in x and ")" not in x else False, split))
        modifier = textStr[textStr.find(
            "(")+1:textStr.find(")")] if textStr.find("(") != -1 else None
        return {
            "character": " ".join(list(character)),
            "modifier": modifier,
            "dialogue": content[index+1][characterType]
        }

    stitchedDialogue = {
        "character1": generateCharacterType(content, i, "segment")
    }

    if "character2" in content[i]:
        stitchedDialogue["character2"] = generateCharacterType(
            content, i, "character2")

    scene["nest"].append(stitchedDialogue)
    return scene


def extractHeader(text):
    def stripWord(textArr): return [x.strip() for x in textArr]
    region = re.match(
        '((?:(?:MONTAGE|FLASHBACK)[ ]?[-][ ]?)?(?:EXT[\.]?\/INT[\.]?|INT[\.]?\/EXT[\.]?|INT\.|EXT\.))', text).groups()[0]
    time = None
    location = text.replace(region, "")
    timeIndex = extractTime(text)
    if timeIndex:
        time = text[timeIndex:].strip("-,. ")
        location = location.replace(time, "")
    return {
        "region": region,
        "location": location.strip("-,. "),
        "time": time
    }


def groupTypes(script, pageStart, pageWidth):
    groupedTypes = []
    scene = {
        "region": None,
        "location": None,
        "time": None,
        "nest": []
    }
    test = False

    for page in script:
        if page["page"] < pageStart:
            continue

        groupedTypes.append({"page": page["page"], "content": []})
        i = 0
        content = page["content"]
        while i < len(content):
            currentTextObj = content[i]

            if determineHeading(currentTextObj["segment"]["text"]):
                if len(scene["nest"]) > 0:
                    groupedTypes[-1]["content"].append(copy.copy(scene))
                heading = extractHeader(
                    currentTextObj["segment"]["text"])
                region = heading["region"]
                location = heading["location"]
                time = heading["time"]
                scene = {
                    "region": region,
                    "location": location,
                    "time": time,
                    "nest": []
                }
            elif determineCharacter(content[i+1]["segment"] if i+1 < len(content) else None, content[i]["segment"], i):
                scene = extractCharacter(
                    scene, content, i)
                i += 1
            else:
                scene["nest"].append({
                    "action": {
                        "text": currentTextObj["segment"]["text"]
                    }
                })

            i += 1
        groupedTypes[-1]["content"].append(copy.copy(scene))
        scene["nest"] = []
        # if page["page"] == 0:
        #     break

    return groupedTypes
