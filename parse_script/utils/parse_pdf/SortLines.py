
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
            key=lambda curr: int(str(curr["y"]) + str(curr["x"])))

        newScript[-1]["content"].sort(
            key=lambda curr: int(str(curr["y"]) + str(curr["x"])))

        for i, content in enumerate(newScript[-1]["content"]):
            if content["y"] - newScript[-1]["content"][i-1]["y"] < 10:
                newScript[-1]["content"][i-1]["y"] = content["y"]
                # print(content)
                # print(newScript[-1]["content"][i-1])
    return newScript
