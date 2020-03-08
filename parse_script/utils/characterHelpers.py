def isParenthetical(text):
    return "(" in text[0] and ")" in text[-1]


def extractCharacter(currentContent):
    text = currentContent["text"]
    split = text.split()
    character = list(
        filter(lambda x: True if "(" not in x and ")" not in x else False, split))
    modifier = text[text.find(
        "(")+1:text.find(")")] if text.find("(") != -1 else None
    return {
        "character": " ".join(list(character)),
        "modifier": modifier,
    }


def isCharacter(currentContent):
    text = currentContent["text"]
    characterNameEnum = ["V.O", "O.S", "CONT'D"]

    if isParenthetical(text):
        return False

    for heading in characterNameEnum:
        if heading in text:
            return True

    if not text[0].isalpha() and "\"" not in text[0]:
        return False

    if text != text.upper():
        return False

    # doc = nlp(text)
    # for token in doc:
    #     if token.pos_ == "VERB" or token.pos_ == "DET":
    #         return False

    # check if header?
    if any(x in text for x in ["--", "!"]):
        return False

    if any(x in text[-1] for x in ["-", "."]):
        return False

    # if not re.search('^[a-zA-Z]+(([\',. -][a-zA-Z ])?[a-zA-Z]*)*$', text):
    #     return False

    return True
