import copy
import json


class GroupTypes:
    def __init__(self, script):
        self.script = script
        self.newScript = []

    headingEnum = ["INT.", "EXT.", "INT./EXT.", "EXT./INT."]

    timeEnum = {
        "DAY": "DAY",
        "NIGHT": "NIGHT",
        "MORNING": "MORNING"
    }

    characterNameEnum = {
        "VOICE_OVER": "V.O.",
        "OFF_SCREEN": "O.S.",
        "CONTINUED": "CONT'D"
    }

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

    @staticmethod
    def determineCharacter(textStr):
        character = textStr.split('(')
        if character[0] != character[0].upper():
            return False

        if len(character) > 1:
            if character[-1].isdigit():
                return True
            if ")" not in character[-1]:
                return False
        elif len(character) == 1:
            if "(" in character[0]:
                return False
        # check if header?
        if "." in character[0]:
            return False
        return True

    def containsParentheticals(self, text):
        return "(" in text[0] and ")" in text[-1]

    def containsDialogue(self, text, y, upperY, x, correctMargin, correctWidth):
        return text.upper() != text and abs(abs(upperY - y) - correctMargin) < 5 and abs(x - correctWidth) < 30

    def extractCharacter(self, scene, currentTextObj, content, i):
        split = currentTextObj["segment"]["text"].split("(")
        modifier = "(" + split[-1] if len(split) > 1 else None
        stitchedDialogue = {
            "character1": {
                "character": split[0].strip(),
                "modifier": modifier,
                "dialogue": content[i+1]["segment"]
            }
        }

        if "character2" in currentTextObj:
            try:
                split = currentTextObj["character2"]["text"].split()
                stitchedDialogue["character2"] = ({
                    "character": split[0],
                    "modifier": split[1] if len(split) > 1 else None,
                    "dialogue": content[i+1]["character2"]
                })
            except:
                print(content[i])
                print(content[i+1])
        scene["nest"].append(stitchedDialogue)

        return scene

    def extractHeader(self, text):
        curr = text.split(".")
        location = []
        time = None
        region = curr[0]
        if len(curr) > 1:
            divider = "."
            dayOrNot = self.determineDay(curr[len(curr) - 1])
            location = curr[1:-1] if dayOrNot else curr

            if (len(curr) == 2):
                divider = ","
                if any("-" in el for el in curr):
                    divider = "-"
                curr = curr[1].split(divider)
                location = curr[0:-1] if dayOrNot else curr

            time = curr[len(curr) - 1] if dayOrNot else None

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
                elif (self.determineCharacter(currentTextObj["segment"]["text"])
                      and i + 1 < len(content) or "character2" in currentTextObj):
                    scene = self.extractCharacter(
                        scene, currentTextObj, content, i)
                    i += 1
                else:
                    scene["nest"].append(currentTextObj)
                i += 1
            groupedTypes[-1]["content"].append(copy.copy(scene))
            scene["nest"] = []
            # if page["page"] == 0:
            #     break

        self.newScript = groupedTypes
