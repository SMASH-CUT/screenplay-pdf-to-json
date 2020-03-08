import json
import re
from parse_pdf.cleanPage import cleanPage


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
            "content": script[i]["content"]
        })
        i += 1

    firstPages = cleanPage(firstPages, 0)
    firstPages = [x for x in firstPages]
    for page in firstPages:
        page["type"] = "FIRST_PAGES"
    return (firstPages, i)
