# I HACKED INTO YOUR ACCOUNT

from utils.characterHelpers import isCharacter
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
    ]
    characters = setupMultiplecharacters(characters)

    expectedcharacters = [
        True,
    ]

    assertGroup(characters, expectedcharacters)


def test_incorrect_characrters():
    characters = [
        'I HACKED INTO YOUR ACCOUNT',
    ]
    characters = setupMultiplecharacters(characters)

    expectedcharacters = [
        False,
    ]

    assertGroup(characters, expectedcharacters)
