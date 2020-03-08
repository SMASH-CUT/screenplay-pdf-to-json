import re

headingEnum = ["EXT./INT.", "INT./EXT.", "INT.", "EXT."]


def isHeading(content):
    text = content["text"]
    for heading in headingEnum:
        if not text.endswith(heading) and heading in text:
            return True
    return False


def extractTime(text):
    findTime = re.search(
        '[-,]?[ ]?(DAWN|DUSK|((LATE|EARLY) )?(NIGHT|AFTERNOON|MORNING)|DAYS|DAY|NIGHT|DAYS|DAY|LATER|NIGHT|SAME|CONTINUOUS|(MOMENTS LATER)|SUNSET)|\d{4}', text)

    time = list(filter(lambda x: len(x) > 0, [x.strip(
        "-,. ") for x in text[findTime.start():].split()])) if findTime else None
    return time


def extractHeading(text):
    def stripWord(textArr): return [x.strip() for x in textArr]

    region = re.search(
        '((?:.* )?(?:EXT[\\.]?\\/INT[\\.]?|INT[\\.]?\\/EXT[\\.]?|INT\\.|EXT\\.))', text).groups()[0]
    time = extractTime(text)

    location = text.replace(region, "")
    if time and len(time) > 0:
        location = location[:location.index(time[0])]

    return {
        "region": region,
        "location": location.strip("-,. "),
        "time": time
    }
