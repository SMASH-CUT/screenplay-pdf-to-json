import copy
import json
import re
import spacy

nlp = spacy.load("en_core_web_sm")


class GroupTypes:
    def __init__(self, script):
        self.script = script
        self.newScript = []

    headingEnum = ["EXT./INT.", "INT./EXT.", "INT.", "EXT."]

    timeEnum = ["DAY", "NIGHT", "MORNING", "DUSK", "LATER"]

    def determineHeading(self, textStr):
        for heading in self.headingEnum:
            if heading in textStr:
                return True
        return False

    def determineDay(self, text):
        for heading in self.timeEnum:
            if heading in text:
                return True
        return False

    def extractDay(self, textStr):
        a = re.search(r'DAY|NIGHT|MORNING', textStr)
        return a.start()

    @staticmethod
    def determineCharacter(nextContent, currentContent,  i):
        textStr = currentContent["text"]
        x = currentContent["x"]
        y = currentContent["y"]
        characterNameEnum = ["V.O", "O.S", "CONT'D"]

        doc = nlp(textStr)
        for token in doc:
            if token.pos_ == "VERB" or token.pos_ == "DET":
                return False

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

        # check if header?
        if "--" in textStr or " - " in textStr or ":" in textStr:
            return False

        # if not re.search('^[a-zA-Z]+(([\',. -][a-zA-Z ])?[a-zA-Z]*)*$', textStr):
        #     return False
        if "END" in textStr or "INC." in textStr:
            return False

        return True

    def containsParentheticals(self, text):
        return "(" in text[0] and ")" in text[-1]

    def containsDialogue(self, text, y, upperY, x, correctMargin, correctWidth):
        return text.upper() != text and abs(abs(upperY - y) - correctMargin) < 5 and abs(x - correctWidth) < 30

    def extractCharacter(self, scene, content, i):
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

    def extractHeader(self, text):
        def stripWord(textArr): return [x.strip() for x in textArr]
        region = re.match(
            '((?:(?:MONTAGE|FLASHBACK)[ ]?[-][ ]?)?(?:EXT[\.]?\/INT[\.]?|INT[\.]?\/EXT[\.]?|INT\.|EXT\.))', text).groups()
        time = None
        if len(text.split('.')) > 2:
            if self.determineDay(text):
                location = region[1:-1]
                time = region[-1]
            else:
                location = region[1:]
            region = region[0]
        else:
            region = region[0]
            if self.determineDay(text):
                location = re.search(
                    "((?:[\w’'() ]+[ ]?[-][ ]?)+(?:(?!\w)))(?![ ]?INT|EXT)", text)
                location = location.groups(
                )[0] if location is not None else None
                time = text.replace(location, "")
                time = time.replace(region, "")
            else:
                location = text.replace(region, "")

        return {
            "region": region,
            "location": location,
            "time": time
        }

    def groupTypes(self, pageWidth):
        groupedTypes = []
        scene = {
            "region": None,
            "location": None,
            "time": None,
            "nest": []
        }
        test = False

        for page in self.script:
            groupedTypes.append({"page": page["page"], "content": []})
            i = 0
            content = page["content"]
            while i < len(content):
                currentTextObj = content[i]

                if self.determineHeading(currentTextObj["segment"]["text"]):
                    if len(scene["nest"]) > 0:
                        groupedTypes[-1]["content"].append(copy.copy(scene))
                    heading = self.extractHeader(
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
                elif self.determineCharacter(content[i+1]["segment"] if i+1 < len(content) else None, content[i]["segment"], i):
                    scene = self.extractCharacter(
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

        self.newScript = groupedTypes
