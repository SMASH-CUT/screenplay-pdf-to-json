


def cleanScript(script, includePageNumber):
    for page in script:
        if not includePageNumber:
            del page["page"]
        for i, section in enumerate(page["content"]):
            for j, scene in enumerate(section["scene"]):
                if type(scene["content"]) is list:
                    for line in scene["content"]:
                        if "x" in line:
                            del line["x"]
                            del line["y"]
                elif "x" in scene["content"]:
                    print(scene)
                    del scene["content"]["x"]
                    del scene["content"]["y"]
    return script