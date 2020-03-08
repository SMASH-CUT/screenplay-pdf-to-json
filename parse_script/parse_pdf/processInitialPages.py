import json
import re


def processInitialPages(script):
    total = []

    for page in script:
        existingY = {}
        for content in page["content"]:
            if content["y"] not in existingY:
                existingY[content["y"]] = True

        total.append(len(existingY))

    avg = sum(total)/len(total)
    firstPages = []
    i = 0
    while i < len(total):
        if total[i] > avg - 10:
            break
        firstPages.append({
            "page": i,
            "type": "FIRST_PAGES",
            "content": {
                "text": script[i]["content"]
            }
        })
        i += 1

    return (firstPages, i)
