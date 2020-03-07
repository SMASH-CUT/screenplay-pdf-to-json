import operator


def getTopTrends(script):
    trends = {}
    for page in script:
        for section in page["content"]:
            roundedX = round(section["segment"][0]["x"])
            if roundedX not in trends:
                trends[roundedX] = 1
            else:
                trends[roundedX] += 1
    trends = sorted(trends.items(), key=operator.itemgetter(0), reverse=False)
    return trends
