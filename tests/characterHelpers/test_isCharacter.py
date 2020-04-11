from screenplay_pdf_to_json.utils import isCharacter
import pytest


def createMockContent(text):
    return {
        "x": 3,
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
    ]
    characters = setupMultiplecharacters(characters)

    expectedcharacters = [
        True,
        True
    ]

    assertGroup(characters, expectedcharacters)


def test_incorrect_characrters():
    characters = [
        'DOING?',
    ]
    characters = setupMultiplecharacters(characters)

    expectedcharacters = [
        False,
    ]

    assertGroup(characters, expectedcharacters)
