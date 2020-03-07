
def sortLines(script, pageStart):
    newScript = []
    for page in script:
        if page["page"] < pageStart:
            continue
        newScript.append({
            "page": page["page"],
            "content": []
        })

        newScript[-1]["content"] = page["content"]

        newScript[-1]["content"].sort(
            key=lambda curr: (curr["y"], curr["x"]))

        # TODO: how to determine this?
        for i, content in enumerate(newScript[-1]["content"]):
            if abs(content["y"] - newScript[-1]["content"][i-1]["y"]) < 5:
                newScript[-1]["content"][i-1]["y"] = content["y"]
        # print(content)
        # print(newScript[-1]["content"][i-1])

        newScript[-1]["content"].sort(
            key=lambda curr: (curr["y"], curr["x"]))

    return newScript
