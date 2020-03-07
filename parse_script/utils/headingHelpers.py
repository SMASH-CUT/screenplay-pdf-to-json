

headingEnum = ["EXT./INT.", "INT./EXT.", "INT.", "EXT."]


def isHeading(content):
    text = content["text"]
    for heading in headingEnum:
        if heading in text:
            return True
    return False


def extractTime(text):
    findTime = re.search(
        '[-,]?[ ]?(DAWN|DUSK|((LATE|EARLY) )?(NIGHT|AFTERNOON|MORNING)|DAYS|DAY|NIGHT|DAYS|DAY|LATER|NIGHT|SAME|CONTINUOUS|(MOMENTS LATER))', text)
    return findTime.start() if findTime else None


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
