

class GroupTypes:
    def __init__(self, script):
        self.script = script
        self.newScript = []

    headingEnum = {
        "INT": "INT",
        "EXT": "EXT",
        "INT_EXT": "INT./EXT.",
        "EXT_INT": "EXT./INT."
    }

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

    def determineHeading(self, textArr):
        for heading in self.headingEnum:
            if heading in textArr[0]:
                return True
        return False

    def determineDay(self, text):
        for heading in self.timeEnum:
            if heading in text:
                return True
        return False

    def determineCharacter(self, textArr):
        # char only have one line
        if len(textArr) > 1:
            return False

        character = textArr[0].split()
        if character[0] != character[0].upper():
            return False

        if len(character) == 1:
            # check if header?
            if "." in character[0]:
                return False
            return True

    def extractCharacter(self, textArr, dialogue, parenthetical):
        split = textArr[0].split()
        return {
            "character": split[0],
            "modifier": split[1] if len(split) > 1 else "",
            "parenthetical": parenthetical if parenthetical else "",
            "dialogue": dialogue
        }

    def extractHeader(self, text):
        curr = text[0].split(".")
        location = []
        time = ""
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
                location = curr[0, -1] if dayOrNot else curr

            time = curr[len(curr) - 1] if dayOrNot else ""

        return {
            "region": region,
            "location": location,
            "time": time
        }

    def groupTypes(self):
        groupedTypes = []
        segment = {
            "region": "",
            "location": "",
            "time": "",
            "nest": []
        }

        for page in self.script:
            groupedTypes.append({"page": page["page"], "content": []})
            i = 0
            content = page["content"]
            while i < len(content):
                currentTextObj = content[i]

                if self.determineHeading(currentTextObj["text"]):
                    groupedTypes[-1]["content"].append(segment)
                    heading = self.extractHeader(currentTextObj["text"])
                    region = heading["region"]
                    location = heading["location"]
                    time = heading["time"]
                    segment = {
                        "region": region,
                        "location": location,
                        "time": time,
                        "nest": []
                    }
                elif self.determineCharacter(currentTextObj["text"]):
                    i += 1
                    print(i)
                    print(content[i])
                    containsParentheticals = len(
                        content[i]["text"]) == 1 and "(" in content[i]["text"][0]
                    if containsParentheticals:
                        segment["nest"].append(self.extractCharacter(
                            currentTextObj["text"], content[i+1], content[i]))
                        i += 1
                    else:
                        segment["nest"].append(self.extractCharacter(currentTextObj["text"], content[i], {
                            "text": [""],
                            "x": 0,
                            "y": 0
                        }))
                else:
                    segment["nest"].append(currentTextObj["text"])
                i += 1

            groupedTypes[-1]["content"].append(segment)
        self.newScript = groupedTypes