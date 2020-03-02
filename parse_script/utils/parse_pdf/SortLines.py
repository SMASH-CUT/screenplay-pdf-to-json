
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
            key=lambda curr: curr["segment"][0]["y"])
    return newScript
