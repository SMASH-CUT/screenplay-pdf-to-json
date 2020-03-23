import spacy
from sys import stderr

try:
    nlp = spacy.load('en')
except OSError:
    print('Downloading language model for the spaCy POS tagger\n'
          "(don't worry, this will only happen once)", file=stderr)
    from spacy.cli import download
    download('en')
    nlp = spacy.load('en')


def isParenthetical(text):
    return "(" in text[0] and ")" in text[-1]


def extractCharacter(currentContent):
    text = currentContent["text"]
    split = text.split()
    modifier = text[text.find(
        "(")+1:text.find(")")] if text.find("(") != -1 else None
    character = text.replace(
        "("+modifier+")", "") if modifier is not None else text
    return {
        "character": character,
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

    # check if header?
    if any(x in text for x in ["--", "!"]):
        return False

    if any(x in text[-1] for x in ["-", "."]):
        return False

    if ")" not in text:
        check = nlp(text)
        for word in check:
            if "VERB" == word.pos_ or "ADP" == word.pos_ or "DET" == word.pos_:
                return False

    return True
