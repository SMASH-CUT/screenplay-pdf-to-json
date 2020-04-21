from screenplay_pdf_to_json.utils import isCharacter
import pytest


def createMockContent(text):
    return {
        "x": 225,
        "y": 4,
        "text": text
    }


def setupMultiplecharacters(characters):
    characters = [createMockContent(heading) for heading in characters]

    characters = [isCharacter(content) for content in characters]
    return characters


def assertGroup(characters, expectedcharacters):
    i = 0
    while i < len(characters):
        assert characters[i] == expectedcharacters[i]
        i += 1


def test_correct_characrters():
    characters = [
        'JOHN',
        'JEFFERSON (INTO P.A.)'
        'D.A.',
        'COBB (reads aloud)'
    ]
    characters = setupMultiplecharacters(characters)

    expectedcharacters = [
        True,
        True,
        True,
        True
    ]

    assertGroup(characters, expectedcharacters)


def test_incorrect_characters():
    characters = [
        'DOING?',
        'CUT BACK TO:',
        'FADE TO BLACK:',
        'I...',
        'I’m Stuart Singer. I’m in your O.S. lab.'
    ]
    characters = setupMultiplecharacters(characters)


    assert isCharacter({
        "x": 180,
        "y": 100,
        "text":  "I WILL SPLIT UP MY FATHER'S",
    }) == False

    expectedcharacters = [
        False,
        False,
        False,
        False,
        False,
        False
    ]

    assertGroup(characters, expectedcharacters)
